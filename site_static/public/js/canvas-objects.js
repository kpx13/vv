$(function(){

  var simpleCanvas = function(id, w, h, obj){
    var stage = new Kinetic.Stage({
      container: id,
      width: w,
      height: h
    });
    var layer = new Kinetic.Layer();
    layer.add(obj);
    stage.add(layer);
  };

  var stageW = 180;
  var stageH = 180;
  
  //Test Geom figures
  
  var geomfig = {
    triangle: new Kinetic.RegularPolygon({
      x: stageW / 2,
      y: stageH / 2 + 18,
      sides: 3,
      radius: 80,
      fill: '#fff',
      stroke: '#444',
      strokeWidth: 2
    }), 
    square: new Kinetic.Rect({
      x: 30,
      y: 30,
      width: 120,
      height: 120,
      fill: 'fff',
      stroke: '444',
      strokeWidth: 2
    }),
    circle: new Kinetic.Circle({
      x: stageW / 2,
      y: stageH / 2,
      radius: 65,
      fill: 'fff',
      stroke: '444',
      strokeWidth: 2
    }),
    rect: new Kinetic.Rect({
      x: 35,
      y: 1,
      width: 90,
      height: 178,
      fill: 'fff',
      stroke: '444',
      strokeWidth: 2
    }),
    line: new Kinetic.Line({        
      points: [38,170, 18,120, 80,178, 30,90, 120,170, 80,50, 150,115, 110,5, 160,85, 165,20 ],
      stroke: '444',
      strokeWidth: 2.2,
      lineJoin: 'round'
    }),
    init: function(){
      simpleCanvas('container', stageW, stageH, geomfig.triangle);
      simpleCanvas('container', stageW, stageH, geomfig.square);
      simpleCanvas('container', stageW, stageH, geomfig.circle);
      simpleCanvas('container', stageW, stageH, geomfig.rect);
      simpleCanvas('container', stageW, stageH, geomfig.line);
    }
  };
  
  geomfig.init();  
  
  //Test Lusher
  
  var lusher = {
    colors: {
      grey: 'rgb(170,170,170)',
      yellow: 'rgb(238,234,0)',
      blue: 'rgb(0,0,200)',
      brown: 'rgb(160,80,10)',
      green: 'rgb(0,170,0)',
      red: 'rgb(240,0,0)',
      purple: 'rgb(170,0,90)',
      black: 'rgb(0,0,0)'
    },
    init: function(){
      for (var i in lusher.colors) {
        lusher.square = new Kinetic.Rect({
          x: 30,
          y: 30,
          width: 140,
          height: 140,
          fill: lusher.colors[i]
        });
        simpleCanvas('container', stageW, stageH, lusher.square);
      }
    }
  };
  
  //lusher.init();
  
  
  
});