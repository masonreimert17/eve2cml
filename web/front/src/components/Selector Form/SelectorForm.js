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
    const clickUpload = ()=>{
      document.getElementById('upload-input').click()
    }
  return (
    <div className="App" >
            
          <h1>Upload Eve File</h1>
          <div className='d-flex justify-content-center'>
          <input id='upload-input' style={{display:'none'}} type="file" onChange={handleChange}/>
          <button className='btn btn-primary' onClick={clickUpload}>Upload</button>
         
          </div>
          </div>
  );
}