from flask import jsonify, redirect, render_template, url_for, flash, request
from app import app
from .forms import UploadForm
import xml.etree.ElementTree as ET
import os
from .helper import parse_events, validate_xml, delete_event_xml, parse_json_events, filter_events
from .globals import uploaded_xml_content, working_file_type
from lxml import etree


@app.route('/')
def index():
    return redirect(url_for('upload_xml'))

# Ruta vizualizare XML
@app.route('/events')
def show_events():
    if working_file_type != 'xml':
        return render_template('redirect.html')

    if len(request.args) == 0:
        events = parse_events(uploaded_xml_content)
        return render_template('events.html', events=events)
    else:
        events = parse_events(uploaded_xml_content)
        print("FROM show_events:" + str(events))
        events = filter_events(events, request.args.get('clientName'), request.args.get('clientType'), request.args.get('startDate'), request.args.get('endDate'))
        print("FROM show_events:" + str(events))
        return render_template('events.html', events=events)

@app.route('/json-events')
def show_json_events():
    if working_file_type == 'json':
        print("FROM json-events: Trying to parse type:" + str(type(uploaded_xml_content)))
        try:
            events = parse_json_events(uploaded_xml_content)
            print("FROM show_events: Showing events as " + str(type(events)))
            return render_template('jsonEvents.html', events=events)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    elif working_file_type == 'xml':
        return redirect(url_for('show_events'))
    else:
        flash('You need to upload an JSON first.', 'warning')
        return render_template('redirect.html')

@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    global uploaded_xml_content
    #print(uploaded_xml_content)
    try:
        uploaded_xml_content = delete_event_xml(uploaded_xml_content, event_id)
        print("Din delete_event: XML MODIFICAT:" + uploaded_xml_content)
        return jsonify({'message': f'Event {event_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload_xml():
    form = UploadForm()
    if form.validate_on_submit():
        print("Formular validat")
        global uploaded_xml_content 
        global working_file_type
        uploaded_file = form.file.data
        uploaded_xml_content = uploaded_file.read()

        filename = uploaded_file.filename
        if filename.endswith('.json'):
            working_file_type = 'json'
            return redirect(url_for('show_json_events'))
        elif filename.endswith('.xml'):
            working_file_type = 'xml'
            return redirect(url_for('show_events'))
        else:
            flash('Fisierul nu este suportat!!!', 'error')
        
    
    return render_template('uploadForm.html', form=form)


@app.route('/view_xml', methods=['GET', 'POST'])
def view_xml():
    global uploaded_xml_content
    global working_file_type
    #print(uploaded_xml_content)
    return render_template('viewXML.html', xml_content=uploaded_xml_content, working_filetype=working_file_type)

@app.route('/validateXML', methods=['POST','GET'])
def validateXML():
    global uploaded_xml_content

    try:
        # Citire date XML
        xml_data = uploaded_xml_content
        
        # Definire path
        dtd_path = "files\events.dtd"
        
        # Existenta DTD
        if not os.path.isfile(dtd_path):
            raise FileNotFoundError(f"DTD file not found at {dtd_path}")
        
        # Citire DTD 
        with open(dtd_path, 'r') as dtd_file:
            dtd_content = dtd_file.read()

        # Validare
        dtd = etree.DTD(ET.fromstring(dtd_content))
        root = ET.fromstring(xml_data)
        
        is_valid = dtd.validate(root)
        
        # Raspuns la http call
        if is_valid:
            response = {'success': True, 'message': 'XML validation successful!'}
        else:
            response = {'success': False, 'message': 'XML validation failed.'}
    except Exception as e:
        response = {'success': True, 'message': f'Error validating XML: {str(e)}'}
    
    return jsonify(response)

@app.route('/eventsXSL')
def show_events_xsl():
    global uploaded_xml_content
    # XML
    xml_data = uploaded_xml_content

    # Incarcare XSL
    xslt_path = 'files/events.xsl'
    xslt = etree.parse(xslt_path)

    if(xml_data):
        xml_tree = etree.fromstring(xml_data)
    else:
        return render_template('redirect.html')
    
    transformer = etree.XSLT(xslt)

    # Aplicare XSL
    html_output = transformer(xml_tree)

    #Template
    return str(html_output) 