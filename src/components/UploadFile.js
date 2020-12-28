import React  from 'react';
import Form  from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
// import useScript from 'useScript';

class UploadFile extends React.Component {
    render() {
        // function handleClick(e) {
        //     e.preventDefault();
        //     // fetch('/get-pdf').then(res => res.json()).then(
        //     //     console.log(res)
        //     // );
        //     fetch('/get-pdf').then(res => res.blob()).then(data => {
        //         console.log(data.info);
        //     });
        // }

        // function start_long_task() {
        //     // add task status elements 
        //     div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
        //     $('#progress').append(div);
    
        //     // create a progress bar
        //     var nanobar = new Nanobar({
        //         bg: '#44f',
        //         target: div[0].childNodes[0]
        //     });
    
        //     // send ajax POST request to start background job
        //     $.ajax({
        //         type: 'POST',
        //         url: '/longtask',
        //         success: function(data, status, request) {
        //             status_url = request.getResponseHeader('Location');
        //             update_progress(status_url, nanobar, div[0]);
        //         },
        //         error: function() {
        //             alert('Unexpected error');
        //         }
        //     });
        // }

        return(
            <div>

            <Form style={{padding: "20px"}} action="/get-pdf" method="post" encType="multipart/form-data">
                
                <Row>
                    <Col className="vertical_align">
                        <label className="col_label">Upload Your Nanopore Target File (.bed extension)</label>
                    </Col>

                    <Col className="vertical_align">
                        <input className="col_value" type="file" accept=".bed" name="target_file" />   
                    </Col>
                </Row>

                <Row>
                    <Col className="vertical_align">
                        <label className="col_label">Upload Your Nanopore VCF File (.vcf extension)</label>
                    </Col>

                    <Col className="vertical_align">
                        <input className="col_value" type="file" accept=".vcf" name="file" />   
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <input style={{display: "inline-block", marginTop: "20px", }} className="submit" type="submit" />
                    </Col>
                </Row>

            </Form>    

                
                {/*
                <Form>
                    <Row>
                        <Col className="vertical_align">
                            <div className="col_label">
                                Upload Your Nanopore Target File (.bed extension)
                            </div>
                        </Col>
                        
                        <Col>
                            <div className = "col_value">
                                <Form.File id="formcheck-api-custom" custom>
                                    <Form.File.Input />
                                        <Form.File.Label data-browse="Browse">
                                        </Form.File.Label>
                                    <Form.Control.Feedback>You did it!</Form.Control.Feedback>
                                </Form.File>    
                            </div>
                        </Col>
                    </Row>
                </Form>   
                */} 
            
            </div>
        );
    }
}

export default UploadFile;
