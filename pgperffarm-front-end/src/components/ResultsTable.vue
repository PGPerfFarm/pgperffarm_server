<template>

	<table class="results">
  		<tr class="results-r">
   			<th class="results-h" colspan="4">
   				Client(s) {{data.clients}}: {{data.median}}

   				<span style="color: #43bb57" v-if="data.percentage > 0.05">
   					<v-icon color="#43bb57">trending_up</v-icon> +{{(data.percentage * 100).toFixed(2)}}%
   				</span>
   			
   				<span style="color: #FF0000" v-else-if="data.percentage < -0.05">
   					<v-icon color="#FF0000">trending_down</v-icon> {{(data.percentage * 100).toFixed(2)}}%
   				</span>

   				<span style="color: #0eb1ee" v-else-if="data.percentage > 0">
   					<v-icon color="#0eb1ee">waves</v-icon> +{{(data.percentage * 100).toFixed(2)}}%
   				</span>

   				<span style="color: #0eb1ee" v-else>
   					<v-icon color="#0eb1ee">waves</v-icon> {{(data.percentage * 100).toFixed(2)}}%
   				</span>
   			</th>
  		</tr>
  		<tr class="results-r">
    		<td class="results-d"> <b> Run </b> </td>
    		<td class="results-d"> <b> Tps </b> </td>
	    	<td class="results-d"> <b> Mode </b> </td>
	    	<td class="results-d"> <b> Latency </b> </td>
  		</tr>
  		<tr class="results-r">
			<td class="results-d"> {{data.run}} </td>
		    <td class="results-d"> {{data.tps}} </td>
		    <td class="results-d"> {{data.mode}} </td>
		    <td class="results-d"> {{data.latency}} </td>
  		</tr>
	</table>

</template>

<script>

	export default {
	  	name: 'ResultsTable',

	  	props: {
    		data: Object
  		},
	}

</script>