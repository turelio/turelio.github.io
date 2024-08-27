console.log("does this work?");
console.log(ing_bool);
function toggle_visibility(id) {
   if (ing_bool[id]==1)
      ing_bool[id]=0;
   else
      ing_bool[id]=1
   console.log(ing_bool);
   var ing = document.getElementById(id);
   if(ing_bool[id]==0)
      ing.style.color = 'grey';
   else
      ing.style.color = 'black';
   redraw()
};

function redraw() {
   for (let key in drink2ing) {
      // console.log(key);
      var possible=1;
      for (const element of drink2ing[key]) {
         // console.log(element);
         if (ing_bool[element]!=1)
            possible=0;
      }
      if (possible==1) {
         drink_bool[key]=1;
         // console.log(`${key} possible`)
      }
      else {
         drink_bool[key]=0;
         console.log(`${key} impossible`)
      }

   }
   console.log(drink_bool)
   for (let key in drink_bool) {
      var box = document.getElementById(key);
      if (drink_bool[key]==1)
         box.style.display="block";
      else
         box.style.display="none";
   }
};
var toggle_all=[1]
function redraw_all() {
      for (let key in ing_bool) {
         if (toggle_all[0]==1) 
            ing_bool[key]=0;
         else
            ing_bool[key]=1;
         var ing = document.getElementById(key);
         if(ing_bool[key]==0)
            ing.style.color = 'grey';
         else
            ing.style.color = 'black';
      }
      if (toggle_all[0]==1)
         toggle_all[0]=0;
      else
         toggle_all[0]=1;
      redraw();
}