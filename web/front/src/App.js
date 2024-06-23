import logo from './logo.svg';
import './App.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import SelectorForm from './components/Selector Form/SelectorForm';
import { useState, useEffect } from 'react';
import { apiGet, downloadFile } from './components/HelperFunctions';

function App() {
  const [backReady, setBackReady] = useState(false)
  
  const [fileDownloadLink, setFileDownloadLink] = useState('')
  // useEffect(() => {
  //   async function fetchData() {
  //     const result = await apiGet('hello');
  //     setHello(result);
  //   }
  //   fetchData();
  // }, []);
 const handleDownloadClick = ()=>{
    downloadFile(fileDownloadLink, 'download.'+fileDownloadLink.split('.').pop())
 }
 const  handleFile=(file)=>{
    const data = new FormData
    data.append('file_from_react', file)
    fetch(window.origin+'/api/ingestFile',{
      method:'post',
      body:data
    }).then(res=>res.json()).then(body=>{
      console.log(body)
      if (body.status === 0){
        console.log("The backend had a oopsies.")
      }
      else{
        let link = window.origin+'/static/'+body['download-url']
        setFileDownloadLink(link)
        setBackReady(true)
        
      }
    })
    
 }
  return (
    <>
      <Navbar className="bg-body-tertiary">
        <Navbar.Brand className='ms-3' href="#home">Converter</Navbar.Brand>
      </Navbar>

      <Container>
          <div className='d-flex justify-content-center'>
          <SelectorForm handleFile={handleFile}/>
        </div>
      </Container>
      {backReady && 
      <>
      
      <p>your download is ready</p>
    <button onClick={handleDownloadClick}>Download</button>
      </>
      }
    </>
  );
}

export default App;
