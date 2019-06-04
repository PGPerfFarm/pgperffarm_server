<template>
	<div class='pg-navbar'>
		<nav>
			<a href='index.html'>Home</a>
			<a href=''>Machine</a>
			<a href=''>Status</a>
			 <div class='dropdown'>
			    <button class='help-button'>Contact
			      <i class='caret-down'></i>
			    </button>
			    <div class="dropdown-content">
			      <a href="#">GitHub</a>
			      <a href="#">License</a>
			      <a href="#">Privacy Policy</a>
			    </div>
			  </div>
		</nav>
	</div>
</template>

<script>
	export default {
		name: 'PgNavbar'
	}
</script>