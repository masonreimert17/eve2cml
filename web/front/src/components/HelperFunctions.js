

function apiBuildOrigin(){
    return window.origin+'/api/'
}

export function apiGet(endpoint){
fetch(apiBuildOrigin()+endpoint).then(req=>req.text())
.then(body=>{
    console.log(body)
    return body
}).catch(err=>console.log(err))

}


export function downloadFile(fileUrl, fileName){
    fetch(fileUrl, {
       //Headers
      }).then((response) => {
          var a = response.body.getReader();
          a.read().then(({ done, value }) => {
              // console.log(new TextDecoder("utf-8").decode(value));
              saveAsFile(value, fileName);
            }
          );
      });
}

function saveAsFile(text, filename) {
    // Step 1: Create the blob object with the text you received
    const type = 'application/text'; // modify or get it from response
    const blob = new Blob([text], {type});
  
    // Step 2: Create Blob Object URL for that blob
    const url = URL.createObjectURL(blob);
  
    // Step 3: Trigger downloading the object using that URL
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click(); // triggering it manually
  }
  export function tableToJson(table) { 
    const headers = [...table.querySelectorAll("thead > tr > th")].map(
        (cell) => cell.innerText
      );
    
      const items = [];
    
      for (const row of table.querySelectorAll("tbody > tr")) {
        const item = {};
    
        for (const [index, cell] of [...row.children].entries()) {
          item[headers[index]] = cell.innerText;
        }
    
        items.push(item);
      }
    
      return items;
}