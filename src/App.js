import React from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom';
import Header from './components/Header';
//import useScript from './components/useScript';
import TestForm from './components/TestForm';
import MyNavbar from './components/MyNavbar';
import Container from 'react-bootstrap/Container';
import About from './components/Pages/about';

// import Nanobar from 'nanobar/nanobar';

import './App.css';

// Bootstrap core CSS 
import './vendor/bootstrap/css/bootstrap.min.css';

// Custom styles for this template
import './css/modern-business.css';
  
// Local CSS
import './css/mycss.css';



function App() {

    return (
        <Router>
            <div>
                <MyNavbar />
                <Route exact path="/" render={props => (
                    <Container>
                        <div className="App">
                            <Header text="Run Report"/>
                            <TestForm />
                        </div>    
                    </Container>
                )} />
                <Route path="/about" component={About} />
                
            </div>
        </Router>
        
        );
}


export default App;
