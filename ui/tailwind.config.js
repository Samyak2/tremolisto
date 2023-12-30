/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
        // color pallete from: https://colorhunt.co/palette/3936464f45576d5d6ef4eee0
				primary: {
					900: '#393646',
					800: '#4F4557',
					700: '#6D5D6E',
          200: 'rgb(158 142 98)',
          100: 'rgb(200 192 171)',
					50: '#F4EEE0'
				}
			}
		}
	},
	plugins: []
};
