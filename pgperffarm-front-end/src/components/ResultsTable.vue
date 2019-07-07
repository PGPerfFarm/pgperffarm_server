<template>

	<v-card>
		<table class="results">
  			<tr>
    			<th colspan="4">
    				Client(s) <!--{{data.clients}}: {{data.median}} {{data.percentage}}-->
    			</th>
  			</tr>
  			<tr>
	    		<td>Run</td>
	    		<td>Tps</td>
	    		<td>Mode</td>
	    		<td>Latency</td>
  			</tr>
  			<tr>
			    <td> {{data.run}} </td>
			    <td>  </td>
			    <td>  </td>
			    <td> {{data.latency}} </td>
  			</tr>
		</table>
	</v-card>

</template>

<script>

	export default {
	  	name: 'ResultsTable',
	  	props: {
    		data: {
        		type: Object
    		}
  		},
	}

</script>