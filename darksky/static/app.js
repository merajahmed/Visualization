$(document).ready(function (){
    var renderer = new THREE.WebGLRenderer({
        antialias: true
    });
    var w = window.innerWidth;
    var h = 600;
    //$(window).height-40;
    renderer.setSize(w, h);
    var halodiv = document.getElementById('halo');
    halodiv.appendChild(renderer.domElement);
    var camera = new THREE.PerspectiveCamera(45, w / h, 1, 10000);
    camera.position.z = 1500;
    camera.position.x = -100;
    camera.position.y = 100;

    var scene = new THREE.Scene();

    var scatterPlot = new THREE.Object3D();
    scene.add(scatterPlot);

    scatterPlot.rotation.y = 0;
    var unfiltered = [];

var format = d3.format("+.3f");
var HaloId = GetParameterValues('HaloId');
var Colormap = GetParameterValues('Colormap');

var particlefile = "static/"+Colormap+"/"+HaloId.toString()+".csv";
var data = d3.csv(particlefile, function (d) {
    
    d.forEach(function (d,i) {
        unfiltered[i] = {
            x: +d.x,
            y: +d.y,
            z: +d.z,
            pr: +d.pr,
            pg: +d.pg,
            pb: +d.pb,
            vr: +d.vr,
            vg: +d.vg,
            vb: +d.vb
            
        };
    })

var xExtent = d3.extent(unfiltered, function (d) {return d.x; }),
    yExtent = d3.extent(unfiltered, function (d) {return d.y; }),
    zExtent = d3.extent(unfiltered, function (d) {return d.z; }),
    pExtent = d3.extent(unfiltered, function (d) {return d.p; });

var vpts = {
    xMax: xExtent[1],
    xCen: (xExtent[1] + xExtent[0]) / 2,
    xMin: xExtent[0],
    yMax: yExtent[1],
    yCen: (yExtent[1] + yExtent[0]) / 2,
    yMin: yExtent[0],
    zMax: zExtent[1],
    zCen: (zExtent[1] + zExtent[0]) / 2,
    zMin: zExtent[0]
}

var colour = d3.scale.category20c();

var xScale = d3.scale.linear()
              .domain(xExtent)
              .range([-600,600]);
var yScale = d3.scale.linear()
              .domain(yExtent)
              .range([-600,600]);                  
var zScale = d3.scale.linear()
              .domain(zExtent)
              .range([-600,600]);


var mat = new THREE.ParticleBasicMaterial({
    vertexColors: true,
    size: 10
});

var pointCount = unfiltered.length;
var pointGeo = new THREE.Geometry();
for (var i = 0; i < pointCount; i ++) {
    var x = xScale(unfiltered[i].x);
    var y = yScale(unfiltered[i].y);
    var z = zScale(unfiltered[i].z);
    pointGeo.vertices.push(new THREE.Vector3(x, y, z));
    //use the following line to color by density of particles
    var Attribute = GetParameterValues('Attribute');
    if (Attribute == 'p')
    	pointGeo.colors.push(new THREE.Color().setRGB(unfiltered[i].pr,unfiltered[i].pg,unfiltered[i].pb));
    else
    	pointGeo.colors.push(new THREE.Color().setRGB(unfiltered[i].vr,unfiltered[i].vg,unfiltered[i].vb));
}
var points = new THREE.ParticleSystem(pointGeo, mat);
scatterPlot.add(points);

renderer.render(scene, camera);
var paused = false;
var last = new Date().getTime();
var down = false;
var sx = 0,
    sy = 0;
    
window.onmousedown = function(ev) {
    down = true;
    sx = ev.clientX;
    sy = ev.clientY;
};
window.onmouseup = function() {
    down = false;
};
window.onmousemove = function(ev) {
    if (down) {
        var dx = ev.clientX - sx;
        var dy = ev.clientY - sy;
        scatterPlot.rotation.y += dx * 0.01;
        camera.position.y += dy;
        sx += dx;
        sy += dy;
    }
}
var animating = false;
window.ondblclick = function() {
    animating = !animating;
    animate(animating);
};

function animate(t) {
    if (!paused) {
        last = t;
        if (animating) {
            var v = pointGeo.vertices;
            for (var i = 0; i < v.length; i++) {
                var u = v[i];
                //console.log(u)
                u.angle += u.speed * 0.01;
                u.x = Math.cos(u.angle) * u.radius;
                u.z = Math.sin(u.angle) * u.radius;
            }
            pointGeo.__dirtyVertices = true;
        }
        renderer.clear();
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
    }
    window.requestAnimationFrame(animate, renderer.domElement);
};
animate(new Date().getTime());
onmessage = function(ev) {
    paused = (ev.data == 'pause');
};

})


});
    function createTextCanvas(text, color, font, size) {
        size = size || 16;
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var fontStr = (size + 'px ') + (font || 'Arial');
        ctx.font = fontStr;
        var w = ctx.measureText(text).width;
        var h = Math.ceil(size);
        canvas.width = w;
        canvas.height = h;
        ctx.font = fontStr;
        ctx.fillStyle = color || 'black';
        ctx.fillText(text, 0, Math.ceil(size * 0.8));
        return canvas;
    }

    function createText2D(text, color, font, size, segW, segH) {
        var canvas = createTextCanvas(text, color, font, size);
        var plane = new THREE.PlaneGeometry(canvas.width, canvas.height, segW, segH);
        var tex = new THREE.Texture(canvas);
        tex.needsUpdate = true;
        var planeMat = new THREE.MeshBasicMaterial({
            map: tex,
            color: 0xffffff,
            transparent: true
        });
        var mesh = new THREE.Mesh(plane, planeMat);
        mesh.scale.set(0.5, 0.5, 0.5);
        mesh.doubleSided = true;
        return mesh;
    }

    function hexToRgb(hex) { //TODO rewrite with vector output
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }


    function v(x, y, z) {
        return new THREE.Vector3(x, y, z);
    }
    
    function GetParameterValues(param) {  
        var url = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');  
        for (var i = 0; i < url.length; i++) {  
            var urlparam = url[i].split('=');  
            if (urlparam[0] == param) {  
                return urlparam[1];  
            }  
        }  
    }  

    function togglemap(){
    	var Colormap = $("#colormap").val();
    	Attribute = GetParameterValues('Attribute');
    	if (Colormap!= GetParameterValues('Colormap')){
    		url = "http://localhost:8000/haloview.html?HaloId="+GetParameterValues('HaloId')+"&&Colormap="+Colormap+"&&Attribute="+Attribute;
    		window.location.assign(url);
    	}
    		
    		
    }
    function toggleattribute(){
    	var Attribute = $("#attribute").val();
    	var Colormap = GetParameterValues('Colormap');
    	if (Attribute!= GetParameterValues('Attribute')){
    		url = "http://localhost:8000/haloview.html?HaloId="+GetParameterValues('HaloId')+"&&Colormap="+Colormap+"&&Attribute="+Attribute;
    		window.location.assign(url);
    	}
    }
    function cmref(){
    	window.open('cmreference.html');
    }
