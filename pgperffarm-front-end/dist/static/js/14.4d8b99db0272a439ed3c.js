webpackJsonp([14],{MG1G:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n={name:"Benchmarks",data:function(){return{panel:[],machines:{},search:"",loading:!0,headers:[{text:"Alias",align:"center",value:"alias"},{text:"Add time",align:"center",value:"add_time"},{text:"Type",align:"center",value:"type"},{text:"Owner",align:"center",value:"owner"},{text:"Count",align:"center",value:"count"},{text:"Trend",align:"center",value:"config_id"}],benchmarks:0}},methods:{all:function(){for(var t=0;t<this.benchmarks;t++)this.panel.push(t)},none:function(){this.panel=[]},getBenchmarks:function(){var t=this,e=new XMLHttpRequest;e.open("GET",this.$store.state.endpoints.benchmarks),e.send(),e.onreadystatechange=function(){if(e.readyState===XMLHttpRequest.DONE)if(200===e.status){for(var a=JSON.parse(e.response),n=0;n<a.length;n++){var s="";s=1==a[n].read_only?"read-only test":"read-write test";var i="Scale "+a[n].scale+", duration "+a[n].duration+", clients "+a[n].clients+", "+s,l={alias:a[n].alias,add_time:a[n].add_time.substring(0,10),type:a[n].machine_type,owner:a[n].username,count:a[n].count,config_id:a[n].pgbench_benchmark_id,id:a[n].machine_id};t.machines.hasOwnProperty(i)||(t.machines[i]=[],t.benchmarks++),t.machines[i].push(l)}t.loading=!1,t.panel.push(0)}else console.log(e.status)}}},mounted:function(){this.getBenchmarks()}},s={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("v-layout",{attrs:{"justify-center":"",column:"","my-4":""}},[a("v-flex",[a("v-card",{staticClass:"pg-v-card",attrs:{flat:""}},[a("v-card-text",{staticClass:"pg-v-card-text-main"},[t._v("\n\t\t\t\tBenchmarks page\n\t\t\t")])],1)],1),t._v(" "),a("v-flex",[a("v-layout",{staticClass:"status-layout",attrs:{column:""}},[a("v-card",{attrs:{flat:""}},[a("v-card-title",{staticClass:"table-title"},[t._v("\n\t\t\t\t\tShown here is the list of different benchmark configurations as well as all machines which reported a run using them. Use the machine link for history of that member on the relevant configuration.\n\t\t\t\t")])],1),t._v(" "),a("v-card",{attrs:{flat:""}},[a("v-col",{staticClass:"text-right"},[a("v-btn",{staticClass:"login-button",on:{click:t.all}},[t._v("All")]),t._v(" "),a("v-btn",{staticClass:"login-button",on:{click:t.none}},[t._v("None")])],1)],1)],1),t._v(" "),a("v-card",{staticClass:"pg-v-card",attrs:{flat:""}},[a("v-expansion-panels",{attrs:{multiple:""},model:{value:t.panel,callback:function(e){t.panel=e},expression:"panel"}},t._l(t.machines,function(e,n){return a("v-expansion-panel",{key:n},[a("v-expansion-panel-header",{staticClass:"panel-div"},[t._v(" "+t._s(n)+" ")]),t._v(" "),a("v-expansion-panel-content",{staticClass:"status-content"},[a("v-card",[[a("v-data-table",{staticClass:"elevation-1",attrs:{headers:t.headers,items:t.machines[n],"hide-default-footer":"",loading:t.loading,"item-key":"alias"},scopedSlots:t._u([{key:"item.alias",fn:function(e){var n=e.item;return[a("router-link",{attrs:{to:{path:"/machine/"+n.id}}},[t._v(" "+t._s(n.alias)+" ")])]}},{key:"item.config_id",fn:function(e){var n=e.item;return[a("router-link",{attrs:{to:{path:"/trend/"+n.id+"/"+n.config_id}}},[t._v(" link ")])]}}],null,!0)})]],2)],1)],1)}),1)],1)],1)],1)},staticRenderFns:[]},i=a("VU/8")(n,s,!1,null,null,null);e.default=i.exports}});
//# sourceMappingURL=14.4d8b99db0272a439ed3c.js.map