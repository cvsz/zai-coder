// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
import type { ThemeApplyOptions, ThemePreference, ThemeState } from '$lib/utils/theme';

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}

	interface Window {
		applyTheme?: (theme?: ThemePreference, options?: ThemeApplyOptions) => ThemeState | null;
	}
}

export {};
