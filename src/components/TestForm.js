import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Row, Col} from 'react-bootstrap';
// import Nanobar from 'react-nanobar';

class TestForm extends React.Component{

    constructor(props) {
        super(props);
    
        this.state = {
            taskStatus : "Nothing submitted",
            taskUrl: 'a url'
        };
    
        this.handleClick = this.handleClick.bind(this);
        this.checkStatus = this.checkStatus.bind(this);
        this.getTaskStatus = this.getTaskStatus.bind(this);
    };
    

    handleClick(e) {
        e.preventDefault();
        const data = new FormData(e.target);
            fetch('/generate-report',{
                method: 'POST',
                body: data
            }).then(res => res.json()).then(data => {
                this.setState({
                    taskStatus : 'Kicked off',
                    taskUrl: data.taskUrl,
                    reportName: data.reportName

                })
                this.getTaskStatus(this, this.state.taskUrl, 1);
            });
    }

    checkStatus() {
        this.setState((state) => {
            return {taskStatus: state.count};
        })
    };  


    getTaskStatus(parent, task, i) {
        setTimeout(function() {
            fetch(task).then(res => res.json()).then(data => {
                parent.setState({
                    taskStatus: data.status
                });
            });
            i++;
            if (i < 10 && parent.state.taskStatus !== 'Complete!') {
                parent.getTaskStatus(parent, task, i);
            }
            else if (parent.state.taskStatus === 'Complete!') {
                parent.getReport(parent.state.reportName);
            }
        
        }, 1000);
    };


    getReport(reportName) {
        const data = {
            'reportName': reportName
        };
        fetch('/get-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
              },
            body: JSON.stringify(data)
        })
        .then(resp => resp.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = reportName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
    };


        render() {
            return (
            <div>
                {/* <Form style={{padding: "20px"}} action={"/get-info"} method="post" encType="multipart/form-data"> */}
                <Form style={{padding: "20px" }} action="#" onSubmit={this.handleClick}>
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
                            <Button type="submit">Submit</Button>
                        </Col>
                    </Row>

                    <div>Current Status: {this.state.taskStatus}</div>
                </Form>

            </div>
            )
        };
    }

export default TestForm;
