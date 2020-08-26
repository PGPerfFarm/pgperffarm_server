<template>
			<v-content>
				<v-layout justify-center column my-4>
					<v-flex>
						<v-card flat class="pg-v-card">
				 			<v-card-text class="pg-v-card-text-main">
								License
							</v-card-text>
						</v-card>
					</v-flex>
					<v-flex>
						<v-card flat class="pg-v-card-bottom">
							<v-card-text class="pg-v-card-text-small">
					  			<p>
									Copyright (c) 2020, The PostgreSQL Global Development Group
								</p>
								<p>
									Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.
								</p>
								<p>
									IN NO EVENT SHALL THE POSTGRESQL GLOBAL DEVELOPMENT GROUP BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE POSTGRESQL GLOBAL DEVELOPMENT GROUP HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
								</p>
								<p>
									THE POSTGRESQL GLOBAL DEVELOPMENT GROUP SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND $ORGANISATION HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
								</p>
							</v-card-text>
						</v-card>
					</v-flex>
			 	</v-layout>
		  	</v-content>
</template>

<script>
	export default {
		name: 'license'
	}
</script>
