require 'pathname'
require 'json'

#
# Usage: ruby scripts/sdk/generate_example_plugins_docs.rb api_samples,example_chart_app,plugins_smoke_test
#

# For local development, allow setting a different location for where to find
# the example plugins. When running in the github action, the workflow will
# clone the canvas-plugins repo within the documentation repo, and this script
# will be invoked from the root of the documentation repo, so the example
# plugins will be found at a relative path of
# './canvas-plugins/example-plugins/'
canvas_plugins_repo_root = ENV['EXAMPLE_PLUGINS_ROOT'] || './canvas-plugins/example-plugins/'

changed_plugins = ARGV[0].split(',')
puts "\nGenerating docs for example plugins:"
changed_plugins.each do |plugin|
  puts "- #{plugin}"
end
puts

changed_plugins.each do |plugin_name|
  plugin_path = Pathname.new("#{canvas_plugins_repo_root}#{plugin_name}")
  unless plugin_path.exist?
    puts "Plugin not found: #{plugin_path}"
    next
  end
  manifest_file = plugin_path.children.select{|a| a.basename.to_s.downcase == 'canvas_manifest.json'}.first
  unless manifest_file
    puts "Directory does not contain a manifest file: #{plugin_path}"
    next
  end

  manifest = JSON.load_file manifest_file
  plugin_name = manifest['name']

  puts "Plugin found: #{plugin_path}"
  File.open("collections/_sdk/examples/#{plugin_name}.md", 'w') do |file|
    file.puts("---")
    file.puts("title: '#{plugin_name}'")
    file.puts("slug: 'example-#{plugin_name}'")
    file.puts("---")
    file.puts("")

    alert_html = <<ALERTHTML
{% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/#{plugin_name}' target='_blank'>View the source</a> for this plugin on GitHub." %}
ALERTHTML

    file.puts()
    file.puts(alert_html)
    file.puts()

    readme = plugin_path.children.select{|a| a.basename.to_s.downcase == 'readme.md'}.first
    readme.readlines.each do |line|
      file.puts(line)
    end
    file.puts()

    def print_directory_contents(directory_path, file, level = 0)
      directory_path.children.sort do |a,b|
        ['readme.md', 'canvas_manifest.json'].include?(a.basename.to_s.downcase) ? 0 : 1
      end.each do |child_path|
        if child_path.directory?
          file.puts("##" + ("#"*level) + " " + child_path.basename.to_s + '/')
          file.puts()
          print_directory_contents(child_path, file, level + 1)
        else
          if child_path.basename.to_s.downcase == 'readme.md'
            # Already handled separately
            next
          end
          file.puts("##" + ("#"*level) + " " + child_path.basename.to_s)
          file.puts()
          if child_path.basename.to_s.downcase == 'canvas_manifest.json'
              file.puts("```json")
              child_path.readlines.each do |line|
                file.puts(line)
              end
              file.puts("```")
              file.puts()
          elsif child_path.extname == ".py"
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

    print_directory_contents plugin_path, file
  end
end

# ```
# ---
# title: "Test Issue 52"
# slug: "example-test-issue-52"
# ---
# 
# {% include alert.html type="github" content="<a href='https://github.com/canvas-medical/canvas-plugins/tree/main/example-plugins/api_samples' target='_blank'>View the source</a> for this plugin on GitHub."  %}
# 
# This is my example
# 
# ## CANVAS_MANIFEST.json
# 
# tktk
# 
# ## routes/
# 
# tk
# 
# ### api.py
# 
# tk
# 
# ### info.py
# 
# tk
# 
# ```
