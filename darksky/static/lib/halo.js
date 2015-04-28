// you can change the file name and the dimensions to be shown
// the colors of PCP polylines are colored by z position by default

var fileName = "static/data/basename.out";

var parcoords = d3.parcoords()("#pcp")
    .alpha(0.4)
    .mode("queue") // progressive rendering
    .height(d3.max([document.body.clientHeight-326, 220]))
    .margin({
      top: 36,
      left: 0,
      right: 0,
      bottom: 16
    });

function print(a){
  console.log(a)
}

var dims, halos;
var dimNum, haloNum;

d3.text(fileName, function(data) {

  // data = data.replace("#", "");
  // var lines = data.split("\n");
  // dims = lines[0].split(" ");
  // dimNum = dims.length;
  // for (var i in dims){
  //   dims[i] = dims[i].toLowerCase();
  // }
  // print (dims)
  // dims = dims.slice(0,23);
  // halos = [];
  // for (var i = 17; i < lines.length - 1; i++){
  //   var row = lines[i];
  //   var col = row.split(" ");
  //   var obj = {}
  //   for (var j = 0; j < dims.length; j++){
  //     obj[dims[j]] = +col[j];
  //   }
  //   halos.push(obj)
  // }
  data = data.replace("#", "");
  var lines = data.split("\n");
  dims = lines[2].split("\t");
  dimNum = dims.length;
  dims = dims.slice(0, dimNum)
  print (dims)
  halos = [];
  for (var i = 3; i < lines.length - 1; i++){
  // for (var i = 3; i <  5; i++){
    var row = lines[i];
    var col = row.split("\t");
    var obj = {}
    for (var j = 0; j < dimNum; j++){
      // print (col[j])
      obj[dims[j]] = +col[j];
    }
    halos.push(obj)
  }

  var COLOR_DIM = dims[5];
  var normalize = d3.scale.linear().range([0,1])
    .domain(d3.extent(halos, function(d) { return d[COLOR_DIM]; }));;

   parcoords
    .data(halos)
    .hideAxis([dims[0]])
    // .hideAxis(["descid"])
    .composite("darker")
    .color(function(d) { return getColor(normalize(d[COLOR_DIM])); })  // quantitative color scale
    .alpha(0.2)
    .render()
    .reorderable()
    .brushMode("1D-axes");

  // setting up grid
  halos.forEach(function(d,i) { d.id = d.id || i; });
  var column_keys = d3.keys(halos[0]);
  print (column_keys)
  var columns = column_keys.map(function(key,i) {
    return {
      id: key,
      name: key,
      field: key,
      sortable: true
    }
  });

  var options = {
    enableCellNavigation: true,
    enableColumnReorder: false,
    multiColumnSort: false
  };

  var dataView = new Slick.Data.DataView();
  var grid = new Slick.Grid("#grid", dataView, columns, options);
  var pager = new Slick.Controls.Pager(dataView, grid, $("#pager"));

  // wire up model events to drive the grid
  dataView.onRowCountChanged.subscribe(function (e, args) {
    grid.updateRowCount();
    grid.render();
  });

  dataView.onRowsChanged.subscribe(function (e, args) {
    grid.invalidateRows(args.rows);
    grid.render();
  });

  // column sorting
  var sortcol = column_keys[0];
  var sortdir = 1;

  function comparer(a, b) {
    var x = a[sortcol], y = b[sortcol];
    return (x == y ? 0 : (x > y ? 1 : -1));
  }
  
  // click header to sort grid column
  grid.onSort.subscribe(function (e, args) {
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;

    if ($.browser.msie && $.browser.version <= 8) {
      dataView.fastSort(sortcol, args.sortAsc);
    } else {
      dataView.sort(comparer, args.sortAsc);
    }
  });

  // highlight row in chart
  grid.onMouseEnter.subscribe(function(e,args) {
    var i = grid.getCellFromEvent(e).row;
    var d = parcoords.brushed() || halos;
    parcoords.highlight([d[i]]);
  });
  grid.onMouseLeave.subscribe(function(e,args) {
    parcoords.unhighlight();
  });
  grid.onClick.subscribe(function(e,args) {
    var i = grid.getCellFromEvent(e).row;
    haloView(halos[i].id);
  });

  // fill grid with halos
  gridUpdate(halos);

  // update grid on brush
  parcoords.on("brush", function(d) {
    gridUpdate(d);
  });

  function gridUpdate(data) {
    dataView.beginUpdate();
    dataView.setItems(data);
    dataView.endUpdate();
  };
});

var ColorMap = chroma.scale("RdYlGn");
function getColor(value){
  if (value < 0){
    print ("false color: " + value)
    return "grey";
  }
  var index = 1 - value;
  return ColorMap(index).hex();
}
function haloView(i){
	 var url = "http://localhost:8000/haloview.html?HaloId="+i.toString();
	 window.open(url);
}