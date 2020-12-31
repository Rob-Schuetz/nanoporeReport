import React  from 'react';
import Form  from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';

class UploadFile extends React.Component {
    render() {


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

            
            </div>
        );
    }
}

export default UploadFile;
