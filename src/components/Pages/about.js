import React from 'react';
import Container from 'react-bootstrap/Container';
import Header from '../Header';


function About() {

    return (
        <Container>
            <Header text="Instructions"/>
            <div style={{padding: "20px"}}>
                
                <h4>Inputs</h4>
                <p style={{fontSize: "16px"}}>
                    This application takes as it's inputs a .vcf file resulting from
                    nanopore sequencing and a .bed file indicating targets of interest
                    for the sequenced tumor sample.
                </p>

                <h4>Output</h4>
                <p style={{fontSize: "16px"}}>
                    This application takes as it's inputs a .vcf file resulting from
                    nanopore sequencing and a .bed file indicating targets of interest
                    for the sequenced tumor sample.
                </p>

            </div>
        </Container>
        
        );
}

export default About;