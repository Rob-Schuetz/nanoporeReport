import React, { useEffect, useState  } from 'react';
import Header from './components/Header';
import UploadFile from './components/UploadFile';

import './App.css';

function App() {
    const [currentTime, setCurrentTime] = useState(0);

    useEffect(() => {
        console.log("Hello world!");
        console.log(fetch('/time1'));
        fetch('/time1').then(res => res.json()).then(data => {
            console.log("Hello!");
            setCurrentTime(data.info);
        });
    }, []);

    return (
            <div className="App">
                <Header />
                <UploadFile />
            </div>
        );
}


// class App extends Component {
//     render() {
//         const [currentTime, setCurrentTime] = useState(0);//[1,"Hello!"];
//         return (
//             <div className="App">
//                 <Header />
//                 <UploadFile />
//                 <p>My info = {setCurrentTime}</p>
//             </div>
//         );
//     }
// }


export default App;
