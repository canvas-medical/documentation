require 'pathname'

# Get the file path from the cli args

events_protobuf_filename = ARGV[0]
if events_protobuf_filename.nil?
  puts "No protobuf input file given."
  puts "Usage: update_events_table.rb <events_protobuf_filename> <events_documentation_markdown_filename>"
  exit 1
end

events_documentation_markdown_filename = ARGV[0]
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
  if inside_event_enum && line.include?('=')
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
# constant and the value is the description.
#
# Now, let's ingest the events table markdown file, associate any pre-existing
# event descriptions and rewrite the table.

in_the_event_table = false

File.foreach(events_documentation_markdown_filename) do |line|

  if in_the_event_table && !line.strip.starts_with?('|')
    puts "out of the event table: #{line}"
    in_the_event_table = false
  end

  if line.strip == '| Event | Description |'
    puts "in the event table: #{line}"
    in_the_event_table = true
    next
  end

  if in_the_event_table
    event, description = line.split('|')
    puts "found event: #{event} with description: #{description}"
    if event_constants.key? event
      puts "the event is present!"
      puts "event: #{event}"
      puts "description: #{description}"
      event_constants[event] = description
    end
  end
end

p event_constants
