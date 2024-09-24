import xml.etree.ElementTree as ET

def calculate_average_fps(xml_file):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Initialize a list to store FPS values
        fps_values = []

        # Loop through the XML structure to find relevant FPS or frame time tags
        # Assume XML contains <frame> tags with <fps> values
        for frame in root.findall('.//frame'):
            fps = frame.find('fps')
            if fps is not None and fps.text.isdigit():
                fps_values.append(float(fps.text))

        # Calculate average FPS
        if fps_values:
            average_fps = sum(fps_values) / len(fps_values)
            return average_fps
        else:
            return None

    except Exception as e:
        print(f"Error processing XML: {e}")
        return None

# Example usage
xml_file = 'performance_log.xml'
average_fps = calculate_average_fps(xml_file)

if average_fps is not None:
    print(f"Average FPS: {average_fps:.2f}")
else:
    print("No FPS data found or an error occurred.")
