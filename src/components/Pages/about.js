import React from 'react';
import Container from 'react-bootstrap/Container';
import Header from '../Header';
import Button from 'react-bootstrap/Button';


function About() {

    return (
        <Container>
            <Header text="Instructions"/>
            <div style={{padding: "20px"}}>
                
                <h4>Inputs</h4>
                <p style={{fontSize: "16px"}}>
                    This application takes as it's inputs a .vcf file resulting from nanopore 
                    sequencing and a .bed file indicating targets of interest for the sequenced 
                    tumor sample. Invalid vcf's will be rejected as long as .bed files that do not 
                    meet the following format (chr, pos-1, pos, target_description). The final 
                    output is a summary of the mutational status at each provided target.
                    <br />
                    <br />
                    <label>Sample .bed file: &nbsp;</label>
                    <form action="/sample-targets" method="post">
                        <Button type="submit" className="redButton">Download sample_targets.bed</Button>
                    </form>
                </p>

                <h4>Output</h4>
                <p style={{fontSize: "16px"}}>
                    This application takes as it's inputs a .vcf file resulting from
                    nanopore sequencing and a .bed file indicating targets of interest
                    for the sequenced tumor sample.  The report is divided into two sections:
                </p>
                <div style={{padding: "10px"}}>
                    <h5>Detected Targets</h5>
                    <p style={{fontSize: "16px"}}>
                        All targets included in this section are present in the provided .vcf file.
                        The mutational status of each present target is indicated in the "Call" column.

                    </p>

                    <h5>Undetected Targets</h5>
                    <p style={{fontSize: "16px"}}>
                        These targets were included in the target .bed file, but was not present in the provided .vcf file.
                    </p>

                </div>


            </div>
        </Container>
        );
}

export default About;