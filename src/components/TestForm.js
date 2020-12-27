import React, { Component, useState, useRef } from 'react';
import Button from 'react-bootstrap/Button';
import Form, { FormLabel } from 'react-bootstrap/Form';
import { Row, Col} from 'react-bootstrap';
import useScript from './../useScript';
// import Nanobar from 'react-nanobar';

function TestForm(props) {

    const [text, setText] = useState("This is the original text");
    const [taskStatus, setTaskStatus] = useState("This is the original status");
    const form = useRef(null);
    let my_info = 'hey';
    

    function handleClick(e) {
        e.preventDefault();
        const data = new FormData(e.target);
        fetch('/generate-report',{
            method: 'POST',
            body: data
        }).then(res => res.json()).then(data => {
            setText(data.taskUrl);
        // fetch('/go-long').then(res => res.json()).then(data => {
        //     setText(data.Location);
        });
    };

    function getTaskStatus(e) {
        e.preventDefault();
        fetch(text).then(res => res.json()).then(data => {
            setTaskStatus(data.status); 
        });
        // if taskStatus  = 'IN PROGRESS'
    };

    function setInfo(entry) {
        console.log(entry);
        entry.preventDefault();
    };


    useScript('//cdnjs.cloudflare.com/ajax/libs/nanobar/0.2.1/nanobar.min.js');
    useScript('//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js');

    // function start_long_task() {
    //     // add task status elements 
    //     const div = <div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div>;
    //     $('#progress').append(div);
    
    //     // create a progress bar
    //     var nanobar = <Nanobar progress={60} />;
    
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
    //             }
    //         });
    //     };

        return(
            <div>
                {/* <Form style={{padding: "20px"}} action={"/get-info"} method="post" encType="multipart/form-data"> */}
                <Form style={{padding: "20px", backgroundColor: "#c1f7e8", }} action="#" onSubmit={handleClick}>
                {/* <Form style={{padding: "20px", backgroundColor: "#c1f7e8", }} action="/go-long" method="post" encType="multipart/form-data" > */}
                {/* <Form style={{padding: "20px"}} action="/get-pdf" method="post" encType="multipart/form-data" /> */}

                    <Row>
                        <Col className="vertical_align">
                            <label className="col_label">Give me a bed</label>
                        </Col>

                        <Col className="vertical_align">
                            <input className="col_value" accept=".bed" type="file" name="test_bed"  />   
                        </Col>
                    </Row>

                    
                    <Row>
                        <Col className="vertical_align">
                            <label className="col_label">Give me a vcf</label>
                        </Col>

                        <Col className="vertical_align">
                            <input className="col_value" accept=".vcf" type="file" name="test_vcf"  />   
                        </Col>
                    </Row>

                    <Row>
                        <Col style={{padding: "20px 0 20px 0",}}>
                            {/* <input style={{display: "inline-block", marginTop: "20px", }} className="submit" type="submit" /> */}
                            <Button type="submit">Button</Button>
                        </Col>
                    </Row>

                    <div>{taskStatus}</div>
                </Form>

                <Form style={{padding: "20px"}} action="#" onSubmit={getTaskStatus}>
                    <Row>
                        <Col className="vertical_align">
                            <Button type="submit">What's the Status?</Button>
                        </Col>
                    </Row>
                </Form>
            </div>
        );
    }

export default TestForm;
