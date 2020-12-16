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
