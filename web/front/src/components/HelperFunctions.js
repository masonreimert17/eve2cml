

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