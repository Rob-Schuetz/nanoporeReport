import React, { Component, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form, { FormLabel } from 'react-bootstrap/Form';
import {Container, Row, Col} from 'react-bootstrap';
import bsCustomFileInput from 'bs-custom-file-input';

class UploadFile extends Component {
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
