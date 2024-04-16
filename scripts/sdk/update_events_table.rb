require 'pathname'

# Get the file path from the cli args

events_protobuf_filename = ARGV[0]
if events_protobuf_filename.nil?
  puts "No protobuf input file given."
  puts "Usage: update_events_table.rb <events_protobuf_filename> <events_documentation_markdown_filename>"
  exit 1
end

events_documentation_markdown_filename = ARGV[1]
if events_documentation_markdown_filename.nil?
  puts "No target documentation file given."
  puts "Usage: update_events_table.rb <events_protobuf_filename> <events_documentation_markdown_filename>"
  exit 1
end

if not Pathname(events_protobuf_filename).exist?
  puts "Could not find file: #{events_protobuf_filename}"
  exit 1
end

if not Pathname(events_documentation_markdown_filename).exist?
  puts "Could not find file: #{events_documentation_markdown_filename}"
  exit 1
end

# Read the file and create an array of event constants.
inside_event_enum = false
event_constants = {}
File.foreach(events_protobuf_filename) do |line|
  if inside_event_enum && line.include?('=') && !line.strip.start_with?('//')
    event_constants[line.split('=')[0].strip] = ""
  end

  if inside_event_enum && line.strip.end_with?('}')
    inside_event_enum = false
  end

  if line.include?('enum EventType')
    inside_event_enum = true
  end
end

# At this point, we have an array of hashes, where the key is the event
# constant and the value is an empty string placeholder for the description.
#
# Now, let's ingest the events table markdown file, associate any pre-existing
# event descriptions and rewrite the table.

in_the_event_table = false

File.foreach(events_documentation_markdown_filename) do |line|

  if in_the_event_table && !line.strip.start_with?('|')
    in_the_event_table = false
  end

  if line.strip == '| Event | Description |'
    in_the_event_table = true
    next
  end

  if in_the_event_table
    line_without_outer_pipes = line.strip.delete_suffix('|').delete_prefix('|')
    event, description = line_without_outer_pipes.split('|')
    event = event.strip
    description = description.strip
    if event_constants.key? event
      event_constants[event] = description
    end
  end
end

# p event_constants

rewritten_table_lines = ['| Event | Description |']
rewritten_table_lines.append('| ----- | ----------- |')
event_constants.each do |event_type, description|
  rewritten_table_lines.append("| #{event_type} | #{description} |")
end

# Now write the new file. This will include all non-table lines from the original file
# and the new table lines from rewritten_table_lines.

File.open("#{File.expand_path(File.dirname(__FILE__))}/events.temp.md", "w+") do |f|
  inside_event_table = false
  new_event_table_written = false
  File.foreach(events_documentation_markdown_filename) do |line|
    if line.strip == '| Event | Description |'
      inside_event_table = true
    end

    if inside_event_table && !line.strip.start_with?('|')
      inside_event_table = false
    end

    if !inside_event_table
      f.puts(line)
    end

    if inside_event_table && ! new_event_table_written
      rewritten_table_lines.each { |element| f.puts(element) }
      new_event_table_written = true
    end

  end
end

puts File.expand_path(File.dirname(__FILE__))