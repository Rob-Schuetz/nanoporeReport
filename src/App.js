import React from 'react';
import Header from './components/Header';
//import useScript from './components/useScript';
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

    return (
        <div>
            <Container>
                <div className="App">
                    <Header />
                    <TestForm />
                </div>    
            </Container>
        </div>
        );
}


export default App;
