<<<<<<< HEAD
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
=======
import React, { Component } from 'react';

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
                <form style={{alignItems: "left", padding: "0 0 10px 0",}} action="/get-pdf" method="post" encType="multipart/form-data">
                    <div style={{width: "100%", display: "inline-block",}}>
                        <label style={{width: "50%", padding: "0 10px 10px 0 ",}}>Upload Your Nanopore Target File (.bed extension)</label>
                        <input style={{width: "50%", display: "inline-block",}} type="file" accept=".bed" name="target_file" />
                    </div>

                    <div style={{width: "100%", display: "inline-block",}}>
                        <label style={{width: "50%", padding: "0 10px 10px 0 ", }}>Upload Your Nanopore VCF (.vcf extension)</label>
                        <input style={{width: "50%", display: "inline-block", padding: "20px 10px 30px 0 "}} accept=".vcf" type="file" name="file" />
                    </div>
                    

                    <input type="submit" />
                </form>
            </div>
        );
    }
}

export default UploadFile;
>>>>>>> 19bcf862de4ddd1af8d7d65f3f744fbf137dfe04
