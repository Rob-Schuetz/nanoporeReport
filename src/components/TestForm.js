import React, { Component, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form, { FormLabel } from 'react-bootstrap/Form';
import { Row, Col} from 'react-bootstrap';

function TestForm() {

    const [text, setText] = useState("This is the original text");
    let my_info = 'hey';
    

    function handleClick(e) {
        e.preventDefault();
        fetch('/get-info').then(res => res.json()).then(data => {
            setText(data.info);
        });
    };

    function setInfo(entry) {
        console.log(entry);
        entry.preventDefault();
    };

        return(
                // <Form style={{padding: "20px"}} action={"/get-info"} method="post" encType="multipart/form-data">
                <Form style={{padding: "20px"}} action="#" onSubmit={setInfo}>

                    <Row>
                        <Col className="vertical_align">
                            <label className="col_label">Give me some celery</label>
                        </Col>

                        <Col className="vertical_align">
                            <input className="col_value" type="text" name="testy"  />   
                        </Col>
                    </Row>

                    <Row>
                        <Col style={{border: "50px",}}>
                            {/* <input style={{display: "inline-block", marginTop: "20px", }} className="submit" type="submit" /> */}
                            <Button type="submit">Button</Button>  
                        </Col>
                    </Row>

                    <div>{text}</div>
                </Form>
        );
    }

export default TestForm;
