import React from 'react';
import Nanobar from 'nanobar';

class ProgressBar extends React.Component {
    
      componentDidMount () {
        var options = {
            classname: 'my-class',
            id: 'my-id',
            target: document.getElementById('progressBar')
        };
    
        const nanobar = this.nanobar = new Nanobar(options);
    
        nanobar.go(this.props.percentage);
      }

      componentDidUpdate(props){
        this.nanobar.go(props.percentage);
    }

    
    
      render () {
        return (
            <div>
                <div id="progressBar"></div>
            </div>
        )
      }
    }

export default ProgressBar;