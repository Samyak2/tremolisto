/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: {
					900: '#393646',
					800: '#4F4557',
					700: '#6D5D6E',
					50: '#F4EEE0'
				}
			}
		}
	},
	plugins: []
};
