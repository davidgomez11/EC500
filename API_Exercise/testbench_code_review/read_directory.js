var fs = require('fs');
var http = require("http");
 
/* 
if (process.argv.length <= 2) {
    console.log("Usage: " + __filename + " path/to/directory");
    process.exit(-1);
}*/
 
var path = process.cwd();

//Function that finds the newly created mp4 and then uploads it to localhost:5000
function finding_file(file) {
	fs.readdir(path, function(err, items) {
    	//console.log(items);
 
    	for (var i=0; i<items.length; i++) {
        	
        	//console.log(items[i]);

        	if (items[i] == file){
        		console.log(items[i])

        		http.createServer(function(request,response){
        			response.writeHead(200,{'Content-Type': 'video/mp4'});
        			var rs = fs.createReadStream(file);
        			rs.pipe(response);
        		}).listen(5000)
        	}
    	}
	});

}



//finding_file('videoplayback.mp4')
finding_file(process.argv[2])




















