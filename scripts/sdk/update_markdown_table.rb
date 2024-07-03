require 'fileutils'
require 'pathname'

# Get the update type (events or effects) from the cli args
update_type = ARGV[0]
markdown_files_dir = "#{File.expand_path(File.dirname(__FILE__), '../..',)}/collections/_sdk"
if update_type == 'events'
  update_markdown_file = "#{markdown_files_dir}/events.md"
  enum_type = 'EventType'
  markdown_table_header = 'Event'
elsif update_type == 'effects'
  update_markdown_file = "#{markdown_files_dir}/effects.md"
  enum_type = 'EffectType'
  markdown_table_header = 'Effect'
else
  puts "First argument must be either 'events' or 'effects'"
  puts "Usage: update_markdown_table.rb <update_type> <protobuf_filename>"
  exit 1
end

protobuf_filename = ARGV[1]
if protobuf_filename.nil?
  puts "No protobuf file given."
  puts "Usage: update_markdown_table.rb <update_type> <protobuf_filename>"
  exit 1
end

if not Pathname(protobuf_filename).exist?
  puts "Could not find file: #{protobuf_filename}"
  exit 1
end

# Read the file and create an array of event constants.
inside_enum = false
enum_constants = {}
File.foreach(protobuf_filename) do |line|
  if inside_enum && line.include?('=') && !line.strip.start_with?('//')
    enum_constants[line.split('=')[0].strip] = ""
  end

  if inside_enum && line.strip.end_with?('}')
    inside_enum = false
  end

  if line.include?("enum #{enum_type}")
    inside_enum = true
  end
end

# At this point, we have an array of hashes, where the key is the enum
# constant and the value is an empty string placeholder for the description.
#
# Now, let's ingest the table from the markdown file, associate any pre-existing
# descriptions and rewrite the table.

in_the_markdown_table = false

File.foreach(update_markdown_file) do |line|

  if in_the_markdown_table && !line.strip.start_with?('|')
    in_the_markdown_table = false
  end

  if line.strip.gsub(' ', '') == "|#{markdown_table_header}|Description|"
    in_the_markdown_table = true
    next
  end

  if in_the_markdown_table
    line_without_outer_pipes = line.strip.delete_suffix('|').delete_prefix('|')
    name, description = line_without_outer_pipes.split('|')
    name = name.strip
    description = description.strip
    if enum_constants.key? name
      enum_constants[name] = description
    end
  end
end

rewritten_table_lines = ["| #{markdown_table_header} | Description |"]
rewritten_table_lines.append('| ----- | ----------- |')
enum_constants.each do |name, description|
  rewritten_table_lines.append("| #{name} | #{description} |")
end

# Now write the new file. This will include all non-table lines from the original file
# and the new table lines from rewritten_table_lines.

temp_file_name = "#{update_type}.temp.md"
temp_file_path = "#{File.expand_path(File.dirname(__FILE__))}/#{temp_file_name}"

File.open(temp_file_path, "w+") do |f|
  inside_table = false
  new_table_written = false
  File.foreach(update_markdown_file) do |line|
    if line.strip == "| #{markdown_table_header} | Description |"
      inside_table = true
    end

    if inside_table && !line.strip.start_with?('|')
      inside_table = false
    end

    if !inside_table
      f.puts(line)
    end

    if inside_table && !new_table_written
      rewritten_table_lines.each { |element| f.puts(element) }
      new_table_written = true
    end

  end
end

# Now overwrite the documentation markdown file and delete the temp file
FileUtils.mv(temp_file_path, update_markdown_file)
