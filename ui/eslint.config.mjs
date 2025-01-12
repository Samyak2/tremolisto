// @ts-check

import globals from 'globals';
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import eslintConfigPrettier from 'eslint-config-prettier';
import eslintPluginSvelte from 'eslint-plugin-svelte';
import * as svelteParser from 'svelte-eslint-parser';

export default tseslint.config(
	eslint.configs.recommended,
	tseslint.configs.recommended,
	eslintConfigPrettier,
	...eslintPluginSvelte.configs['flat/recommended'],
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				parser: tseslint.parser,
				project: 'tsconfig.json',
				extraFileExtensions: ['.svelte']
			}
		}
	},
	{
		languageOptions: {
			globals: {
				...globals.node
			}
		}
	},
	{
		// Note: there should be no other properties in this object
		ignores: ['build/*', '.svelte-kit/*', 'node_modules/*']
	}
);
