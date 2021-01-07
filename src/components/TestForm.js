import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { Row, Col} from 'react-bootstrap';
import ProgressBar from './ProgressBar';
     

class TestForm extends React.Component{

    constructor(props) {
        super(props);
    
        this.state = {
            taskStatus : "Nothing submitted",
            taskUrl: 'a url',
            percentage: 0,
            runTime: 0,
            showStatus: false
        };
    
        this.handleClick = this.handleClick.bind(this);
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
                    reportName: data.reportName,
                    myTaskId: data.my_id,
                    showStatus: true,
                    showProgressBar: true
                })
                this.getTaskStatus(this, this.state.taskUrl, this.state.myTaskId, this.state.reportName, 1);
            });
    }


    getTaskStatus(parent, task, myTaskId, reportName, i) {
        const data = {
            'my_id': myTaskId
        };
        setTimeout(function() {
            fetch(task, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify(data)
            }).then(res => res.json()).then(data => {
                parent.setState({
                    taskStatus: data.status,
                    percentage: data.percentage,
                    runTime: (i/2).toFixed(1)
                });
            });
            i++;
            if (i < 40 && parent.state.taskStatus !== 'Complete!') {
                parent.getTaskStatus(parent, task, myTaskId, reportName, i);
            }
            else if (parent.state.taskStatus === 'Complete!') {
                parent.setState({
                    runTime: i/2,
                    percentage: 100
                })
                parent.getReport(parent.state.reportName);
                setTimeout(function() {
                    parent.setState({
                    showProgressBar: false
                })}, 1000);
            }
        
        }, 500);
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
                            <label className="col_label">Upload target file (.bed extension)</label>
                        </Col>

                        <Col className="vertical_align">
                            <input className="col_value" accept=".bed" type="file" name="test_bed"  />   
                        </Col>
                    </Row>

                    
                    <Row>
                        <Col className="vertical_align">
                            <label className="col_label">Upload variant file (.vcf extension)</label>
                        </Col>

                        <Col className="vertical_align">
                            <input className="col_value" accept=".vcf" type="file" name="test_vcf"  />   
                        </Col>
                    </Row>

                    <Row>
                        <Col style={{padding: "20px 0 20px 0",}}>
                            {/* <input style={{display: "inline-block", marginTop: "20px", }} className="submit" type="submit" /> */}
                            <Button type="submit" className="redButton">Submit</Button>
                        </Col>
                    </Row>

                    { this.state.showStatus ?
                        <div>
                            <div>Task Status: {this.state.taskStatus}</div>
                            { this.state.showProgressBar ? <ProgressBar percentage={this.state.percentage} /> : null}
                            <div>Run Time: {this.state.runTime} seconds</div>
                        </div>
                        : null }
                    {/* <div>Percent Complete: {this.state.percentage}%</div> */}
                    {/* <ProgressBar percentage = {this.state.percentage}/> */}
                </Form>

            </div>
            )
        };
    }

export default TestForm;
