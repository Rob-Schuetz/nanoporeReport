import React, { useEffect, useState  } from 'react';
import Header from './components/Header';
import UploadFile from './components/UploadFile';
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

    useEffect(() => {
        fetch('/time1').then(res => res.json()).then(data => {
            setCurrentTime(data.info);
        });
    }, []);

    return (
            <Container>
                <div className="App">
                    <Header />
                    <UploadFile />
                </div>    
            </Container>
        );
}


export default App;
