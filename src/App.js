import React, { useEffect, useState  } from 'react';
import Header from './components/Header';
import UploadFile from './components/UploadFile';
import TestForm from './components/TestForm';
import Container from 'react-bootstrap/Container';

import './App.css';

// Bootstrap core CSS 
import './vendor/bootstrap/css/bootstrap.min.css';

// Custom styles for this template
import './css/modern-business.css';
  
// Local CSS
import './css/mycss.css';



function App() {
    const [currentTime, setCurrentTime] = useState(0);
    const [currentInfo, setCurrentInfo] = useState(0);

    useEffect(() => {
        fetch('/time1').then(res => res.json()).then(data => {
            setCurrentTime(data.info);
        });
        fetch('/get-info').then(res => res.json()).then(data => {
            setCurrentInfo(data.info);
        });
    }, []);
    
    // useEffect(() => {
    //     fetch('/get-info').then(res => res.json()).then(data => {
    //         setCurrentTime(data.info);
    //     });
    // }, []);


    // function handleClick(e) {
    //     e.preventDefault();
    //         fetch('/get-info').then(res => res.json()).then(data => {
    //             setCurrentInfo(data.info);
    //     });



    return (
        <div>
            <Container>
                <div className="App">
                    <Header />
                    <UploadFile />
                    {/*<TestForm />
                    <div>
                        Here's the info: { currentInfo }
                    </div>*/}
                </div>    
            </Container>
        </div>
        );
}


export default App;
