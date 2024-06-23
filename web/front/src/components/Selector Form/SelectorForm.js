import React, {useEffect, useState} from 'react';
import { apiGet } from '../HelperFunctions';


export default function SelectorForm({handleFile}){
    const [file, setFile] = useState()
    
  function handleChange(event) {
    event.preventDefault()
    let selectedFile = event.target.files[0]
    setFile(selectedFile)
    
    handleFile(selectedFile)
  }
    
  return (
    <div className="App">
            
          <h1>Upload Eve File</h1>
          <div className='d-flex'>
          <input type="file" onChange={handleChange}/>
          {!file ? '' : <button >Upload</button>}
          
          </div>
          </div>
  );
}