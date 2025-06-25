require "net/http"
require 'json'
require 'pathname'

#
# Usage: ruby scripts/sdk/generate_example_plugins_docs.rb api_samples,example_chart_app,plugins_smoke_test
#

# For local development, allow setting a different location for where to find
# the example plugins. When running in the github action, the workflow will
# clone the canvas-plugins repo within the documentation repo, and this script
# will be invoked from the root of the documentation repo, so the example
# plugins will be found at a relative path of
# './canvas-plugins/example-plugins/'
CANVAS_PLUGINS_REPO_ROOT = ENV['EXAMPLE_PLUGINS_ROOT'] || './canvas-plugins/example-plugins/'

OPENAI_API_KEY = ENV['OPENAI_API_KEY']

# List the plugins we were requested to generate docs for
changed_plugins = ARGV[0].split(',')
puts "\nGenerating docs for example plugins:"
changed_plugins.each do |plugin|
  puts "- #{plugin}"
end
puts

# Define a method to get an external consultation on what a file's purpose is
def get_llm_explanation_of_python_code(python_file)
  filename = python_file.basename.to_s
  file_content = python_file.readlines.join

  # Fake the output if we don't have an API key set (for debugging/local dev)
  if OPENAI_API_KEY.nil?
    response_json = [
        {
            "id": "msg_abc123",
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": "This file is great.",
                    "annotations": []
                }
            ]
        },
        {
            "id": "msg_def456",
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": "It does lots of neat stuff.",
                    "annotations": []
                }
            ]
        }
    ]
  else
    uri = URI('https://api.openai.com/v1/responses')

    body = {
      instructions: "This is #{filename}. It is included in a plugin built using the Canvas SDK, whose documentation can be found at https://docs.canvasmedical.com. What does the code in this file do? Give me markdown output, but with no headers or horizontal lines. Instead of headers, separate sections with bold titles.",
      model: 'gpt-4.1',
      input: file_content
    }

    headers = {
      'Content-Type': 'application/json',
      'Authorization': "Bearer #{OPENAI_API_KEY}"
    }

    response = Net::HTTP.post(uri, body.to_json, headers)
    response_json = JSON.parse(response.body)
  end

  outputs = response_json['output'].map{|output| output['content'].select{|content| content['type'] == 'output_text'}.map{|output| output['text']}.join("\n")}.join("\n")
  return outputs
end

# For each plugin
changed_plugins.each do |plugin_name|
  # See if there is a matching plugin directory in the canvas plugins repo
  plugin_path = Pathname.new("#{CANVAS_PLUGINS_REPO_ROOT}#{plugin_name}")
  unless plugin_path.exist?
    puts "Plugin not found: #{plugin_path}"
    next
  end
  # If the directory exists, see if it contains a manifest file
  manifest_file = plugin_path.children.select{|a| a.basename.to_s.downcase == 'canvas_manifest.json'}.first
  unless manifest_file
    puts "Directory does not contain a manifest file: #{plugin_path}"
    next
  end

  # Load the manifest file, and read the name attribute (which we use a lot)
  manifest = JSON.load_file manifest_file
  plugin_name = manifest['name']

  puts "Plugin found: #{plugin_path}"

  # Write or overwrite a markdown file that will contain our documentation
  File.open("collections/_sdk/examples/#{plugin_name}.md", 'w') do |file|
    # Add the front matter
    file.puts("---")
    file.puts("title: '#{plugin_name}'")
    file.puts("slug: 'example-#{plugin_name}'")
    file.puts("---")
    file.puts("")

    # Add a banner with a link to the plugin's location in the github repo
    alert_html = <<ALERTHTML
{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/#{plugin_name}' target='_blank'>View the source</a> for this plugin on GitHub." %}
ALERTHTML
    file.puts(alert_html)
    file.puts()

    # Embed the readme markdown content directly into this doc page
    readme = plugin_path.children.select{|a| a.basename.to_s.downcase == 'readme.md'}.first
    readme.readlines.each do |line|
      file.puts(line)
    end
    file.puts()

    # This is a method which is called recursively to walk the plugin
    # directory structure. It recreates the tree as nested headers, which are
    # used to generate the table of contents.
    # 
    # Some files may be listed as a header but without having their content
    # displayed. We only display content of the manifest and files ending in .py.
    def print_directory_contents(directory_path, file, level = 0)
      # We sort the files to ensure the readme and manifest are handled first.
      directory_path.children.sort do |a,b|
        ['readme.md', 'canvas_manifest.json'].include?(a.basename.to_s.downcase) ? 0 : 1
      end.each do |child_path|
        # If the current child_path is a directory, we'll create the header
        # for the directory and then recurse.
        if child_path.directory?
          file.puts("##" + ("#"*level) + " " + child_path.basename.to_s + '/')
          file.puts()
          print_directory_contents(child_path, file, level + 1)
        else
          # Ignore the readme, we dumped its contents above
          if child_path.basename.to_s.downcase == 'readme.md'
            # Already handled separately
            next
          end
          # Create a header at the appropriate level (starting with h2) for
          # this filename.
          file.puts("##" + ("#"*level) + " " + child_path.basename.to_s)
          file.puts()
          # If its the manifest file, ensure the syntax highlighting is set to
          # json when dumping the contents.
          if child_path.basename.to_s.downcase == 'canvas_manifest.json'
            file.puts("```json")
            child_path.readlines.each do |line|
              file.puts(line)
            end
            file.puts("```")
            file.puts()
          # If it's a python file, ensure the syntax highlighting is set to
          # python when dumping the contents
          elsif child_path.extname == ".py"
            file.puts(get_llm_explanation_of_python_code(child_path))
            file.puts()
            file.puts("```python")
            child_path.readlines.each do |line|
              file.puts(line)
            end
            file.puts("```")
            file.puts()
          end
        end
      end
    end

    # Initial entrypoint for the recursive function
    print_directory_contents plugin_path, file

    # Ensure padding at the bottom of the page
    file.puts("<br/>")
    file.puts("<br/>")
    file.puts("<br/>")
  end
end
