import xml.etree.ElementTree as ET
from lxml import etree
import json
import os

def validate_xml(xml_input, dtd_input):
    try:
        if os.path.isfile(xml_input):
            with open(xml_input, 'r') as f:
                xml_content = f.read()
        else:
            xml_content = xml_input
        
        if os.path.isfile(dtd_input):
            with open(dtd_input, 'r') as f:
                dtd_content = f.read()
        else:
            dtd_content = dtd_input
        
        xml_tree = etree.fromstring(xml_content)
        
        dtd = etree.DTD(etree.fromstring(dtd_content))
        
        is_valid = dtd.validate(xml_tree)
        
        if is_valid:
            return xml_tree
        else:
            return "XML file is not valid"
    except Exception as e:
        return f"Error: {e}"

 # Function to parse the XML file and extract event data
def parse_events(xml_file):
        root = {}
        root = ET.fromstring(xml_file)
        print('Wrong type in parse_event (path/content)')
        
        events = []
        for event in root.findall('event'):
            event_data = {'status': event.get('status')} 
            for child in event:
                if child.tag == 'menu':
                    menu_data = {}
                    for menu_item in child:
                        if menu_item.tag in ['appetizer', 'mainCourse', 'dessert']:
                            menu_data[menu_item.tag] = {sub_child.tag: sub_child.text for sub_child in menu_item}
                    event_data['menu'] = menu_data
                elif child.tag == 'pricing':
                    event_data[child.tag] = {sub_child.tag: sub_child.text for sub_child in child}
                else:
                    event_data[child.tag] = child.text
            events.append(event_data)
        return events

def parse_json_events(json_file):
    try:
        root = json.loads(json_file)
        if not isinstance(root, dict):
            raise ValueError('Invalid JSON format')
        
        # Extract data from JSON and prepare it for rendering in the template
        events = []
        for event in root.get('events', []):
            event_data = {}
            for key, value in event.items():
                if key == 'menu':
                    menu_data = {}
                    for menu_item_key, menu_item_value in value.items():
                        if menu_item_key in ['appetizer', 'mainCourse', 'dessert']:
                            menu_data[menu_item_key] = {sub_key: sub_value for sub_key, sub_value in menu_item_value.items()}
                    event_data['menu'] = menu_data
                elif key == 'pricing':
                    event_data[key] = {sub_key: sub_value for sub_key, sub_value in value.items()}
                else:
                    event_data[key] = value
            events.append(event_data)
        return events
    except Exception as e:
        print(f'Error in parsing JSON: {e}')
        return []
    
def save_xml(xml_content, file_name, saving_path):
    try:
        # If the xml_content is a path to a file, read the content
        if os.path.isfile(xml_content):
            with open(xml_content, 'rb') as file:
                xml_content = file.read()

        # Construct the file path
        file_path = os.path.join(saving_path, file_name)

        # Write the XML content to the file
        with open(file_path, 'wb') as file:
            file.write(xml_content)

        return 'XML file saved successfully'
    except Exception as e:
        return f'Error saving XML file: {e}'
def delete_event_xml(xml, event_id):
    try:
        print("Din delete_event_xml: Trying to delete element with ID:", event_id)
        root = ET.fromstring(xml)
        print("am trecut de parse")
        
        
        # Find the event with the specified ID
        event_to_delete = None
        for event in root.findall('event'):
            if event.find('id').text == str(event_id):
                event_to_delete = event
                break
        
        # If the event is found, remove it from the XML
        if event_to_delete is not None:
            root.remove(event_to_delete)
            # Return the modified ElementTree object
            print("Din delete_event_xml: Am modificat XML:")
            print(root)
            return root
        else:
            return None  # Event not found
    except Exception as e:
        print("Error:", e)
        return None
    
def filter_events(events, client_name=None, client_type=None, start_date=None, end_date=None):
    filtered_events = []
    for event in events:

        if client_name and client_name.lower() not in event.get('clientName', '').lower():
            continue
        

        if client_type and event.get('type', '').lower() != client_type.lower():
            continue
        

        if start_date and event.get('date') < start_date:
            continue
        if end_date and event.get('date') > end_date:
            continue
        
        filtered_events.append(event)
    
    return filtered_events