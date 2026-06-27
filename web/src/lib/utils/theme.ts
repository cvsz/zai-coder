export type ThemePreference = 'system' | 'light' | 'dark';
export type ThemeMode = 'light' | 'dark';

export type ThemeTokens = {
	background: string;
	backgroundElevated: string;
	surface: string;
	surfaceElevated: string;
	panel: string;
	card: string;
	border: string;
	borderStrong: string;
	text: string;
	textMuted: string;
	textSubtle: string;
	accent: string;
	accentContrast: string;
	success: string;
	warning: string;
	danger: string;
	info: string;
	focus: string;
	selection: string;
	overlay: string;
	backdrop: string;
	scrollbarThumb: string;
	tooltip: string;
	popover: string;
	modal: string;
	drawer: string;
	nav: string;
	sidebar: string;
	commandPalette: string;
	chatBubbleUser: string;
	chatBubbleAssistant: string;
	editor: string;
	codeBlock: string;
	codeText: string;
	syntaxKeyword: string;
	syntaxString: string;
	syntaxComment: string;
	syntaxFunction: string;
	syntaxType: string;
	splash: string;
};

export type ThemeState = {
	preference: ThemePreference;
	resolved: ThemeMode;
	tokens: ThemeTokens;
};

export type ThemeApplyOptions = {
	animate?: boolean;
	persist?: boolean;
	storage?: Storage | null;
	document?: Document | null;
	prefersDark?: boolean;
};

export type ThemeControllerOptions = ThemeApplyOptions & {
	initialTheme?: unknown;
	onApply?: (state: ThemeState) => void;
};

export const THEME_STORAGE_KEY = 'theme';
export const THEME_CLASSNAMES: ThemeMode[] = ['light', 'dark'];
export const THEME_PREFERENCES: ThemePreference[] = ['system', 'light', 'dark'];

const LEGACY_THEME_MAP: Record<string, ThemePreference> = {
	'oled-dark': 'dark',
	her: 'light'
};

const THEME_VARIABLE_MAP: Record<keyof ThemeTokens, string> = {
	background: '--app-background',
	backgroundElevated: '--app-background-elevated',
	surface: '--app-surface',
	surfaceElevated: '--app-surface-elevated',
	panel: '--app-panel',
	card: '--app-card',
	border: '--app-border',
	borderStrong: '--app-border-strong',
	text: '--app-foreground',
	textMuted: '--app-muted',
	textSubtle: '--app-muted-strong',
	accent: '--app-accent',
	accentContrast: '--app-accent-contrast',
	success: '--app-success',
	warning: '--app-warning',
	danger: '--app-danger',
	info: '--app-info',
	focus: '--app-focus',
	selection: '--app-selection',
	overlay: '--app-overlay',
	backdrop: '--app-backdrop',
	scrollbarThumb: '--app-scrollbar-thumb',
	tooltip: '--app-tooltip',
	popover: '--app-popover',
	modal: '--app-modal',
	drawer: '--app-drawer',
	nav: '--app-nav',
	sidebar: '--app-sidebar',
	commandPalette: '--app-command-palette',
	chatBubbleUser: '--app-chat-bubble-user',
	chatBubbleAssistant: '--app-chat-bubble-assistant',
	editor: '--app-editor',
	codeBlock: '--app-code-block',
	codeText: '--app-code-text',
	syntaxKeyword: '--app-syntax-keyword',
	syntaxString: '--app-syntax-string',
	syntaxComment: '--app-syntax-comment',
	syntaxFunction: '--app-syntax-function',
	syntaxType: '--app-syntax-type',
	splash: '--app-splash'
};

const LIGHT_TOKENS: ThemeTokens = {
	background: '#f4f7fb',
	backgroundElevated: '#eef3f9',
	surface: 'rgba(255, 255, 255, 0.82)',
	surfaceElevated: '#ffffff',
	panel: '#f8fafc',
	card: '#ffffff',
	border: 'rgba(148, 163, 184, 0.24)',
	borderStrong: 'rgba(100, 116, 139, 0.32)',
	text: '#0f172a',
	textMuted: '#475569',
	textSubtle: '#64748b',
	accent: '#2563eb',
	accentContrast: '#ffffff',
	success: '#16a34a',
	warning: '#d97706',
	danger: '#dc2626',
	info: '#0ea5e9',
	focus: '#2563eb',
	selection: 'rgba(37, 99, 235, 0.18)',
	overlay: 'rgba(15, 23, 42, 0.24)',
	backdrop: 'rgba(15, 23, 42, 0.6)',
	scrollbarThumb: 'rgba(100, 116, 139, 0.34)',
	tooltip: '#0f172a',
	popover: '#ffffff',
	modal: '#ffffff',
	drawer: '#f8fafc',
	nav: '#ffffff',
	sidebar: '#f8fafc',
	commandPalette: '#ffffff',
	chatBubbleUser: '#dbeafe',
	chatBubbleAssistant: '#eef2ff',
	editor: '#ffffff',
	codeBlock: '#0f172a',
	codeText: '#e2e8f0',
	syntaxKeyword: '#c026d3',
	syntaxString: '#059669',
	syntaxComment: '#94a3b8',
	syntaxFunction: '#2563eb',
	syntaxType: '#7c3aed',
	splash: '#f2f5fa'
};

const DARK_TOKENS: ThemeTokens = {
	background: '#090d12',
	backgroundElevated: '#0f1520',
	surface: 'rgba(13, 18, 27, 0.86)',
	surfaceElevated: '#121a27',
	panel: '#0f1722',
	card: '#111827',
	border: 'rgba(148, 163, 184, 0.18)',
	borderStrong: 'rgba(148, 163, 184, 0.28)',
	text: '#e2e8f0',
	textMuted: '#94a3b8',
	textSubtle: '#cbd5e1',
	accent: '#60a5fa',
	accentContrast: '#08111f',
	success: '#4ade80',
	warning: '#fbbf24',
	danger: '#f87171',
	info: '#38bdf8',
	focus: '#93c5fd',
	selection: 'rgba(96, 165, 250, 0.22)',
	overlay: 'rgba(2, 6, 23, 0.56)',
	backdrop: 'rgba(2, 6, 23, 0.76)',
	scrollbarThumb: 'rgba(148, 163, 184, 0.38)',
	tooltip: '#020617',
	popover: '#111827',
	modal: '#0f1520',
	drawer: '#0b1220',
	nav: '#0b1220',
	sidebar: '#0b1220',
	commandPalette: '#0b1220',
	chatBubbleUser: '#172554',
	chatBubbleAssistant: '#111827',
	editor: '#09111d',
	codeBlock: '#050816',
	codeText: '#e2e8f0',
	syntaxKeyword: '#f472b6',
	syntaxString: '#4ade80',
	syntaxComment: '#64748b',
	syntaxFunction: '#93c5fd',
	syntaxType: '#c084fc',
	splash: '#06090f'
};

let themeTransitionTimeout: number | undefined;

export function normalizeThemePreference(value: unknown): ThemePreference {
	const normalized = String(value ?? 'system').trim().toLowerCase();
	if (normalized in LEGACY_THEME_MAP) {
		return LEGACY_THEME_MAP[normalized];
	}

	if (THEME_PREFERENCES.includes(normalized as ThemePreference)) {
		return normalized as ThemePreference;
	}

	return 'system';
}

export function isPrefersDarkMode(preference: unknown = 'system'): boolean {
	return getResolvedTheme(preference) === 'dark';
}

export function getResolvedTheme(
	preference: unknown = 'system',
	prefersDark = typeof window !== 'undefined' &&
		typeof window.matchMedia === 'function' &&
		window.matchMedia('(prefers-color-scheme: dark)').matches
): ThemeMode {
	const normalized = normalizeThemePreference(preference);
	return normalized === 'system' ? (prefersDark ? 'dark' : 'light') : normalized;
}

export function getThemeTokens(resolvedTheme: ThemeMode): ThemeTokens {
	return resolvedTheme === 'dark' ? DARK_TOKENS : LIGHT_TOKENS;
}

function applyThemeTransition(root: HTMLElement, animate: boolean) {
	if (!animate || typeof window === 'undefined') {
		return;
	}

	if (window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
		return;
	}

	root.classList.add('theme-transitioning');
	if (themeTransitionTimeout !== undefined) {
		window.clearTimeout(themeTransitionTimeout);
	}

	themeTransitionTimeout = window.setTimeout(() => {
		root.classList.remove('theme-transitioning');
		themeTransitionTimeout = undefined;
	}, 220);
}

export function applyThemePreference(
	preference: unknown,
	{ animate = false, document: doc = typeof document !== 'undefined' ? document : null, prefersDark }: ThemeApplyOptions = {}
): ThemeState | null {
	if (!doc) {
		return null;
	}

	const root = doc.documentElement;
	const normalized = normalizeThemePreference(preference);
	const resolved = getResolvedTheme(normalized, prefersDark);
	const tokens = getThemeTokens(resolved);

	root.dataset.themePreference = normalized;
	root.dataset.themeResolved = resolved;
	root.classList.remove(...THEME_CLASSNAMES);
	root.classList.add(resolved);
	root.style.colorScheme = resolved;

	for (const [tokenName, cssVar] of Object.entries(THEME_VARIABLE_MAP) as Array<
		[keyof ThemeTokens, string]
	>) {
		root.style.setProperty(cssVar, tokens[tokenName]);
	}

	const metaThemeColor = doc.querySelector<HTMLMetaElement>('meta[name="theme-color"]');
	if (metaThemeColor) {
		metaThemeColor.setAttribute('content', tokens.splash);
	}

	applyThemeTransition(root, animate);

	return {
		preference: normalized,
		resolved,
		tokens
	};
}

export function createThemeController({
	document: doc = typeof document !== 'undefined' ? document : null,
	storage = typeof window !== 'undefined' ? window.localStorage : null,
	initialTheme = storage?.getItem(THEME_STORAGE_KEY) ?? 'system',
	animate = false,
	onApply
}: ThemeControllerOptions = {}) {
	let preference = normalizeThemePreference(initialTheme);
	const prefersDark = () =>
		typeof window !== 'undefined' &&
		typeof window.matchMedia === 'function' &&
		window.matchMedia('(prefers-color-scheme: dark)').matches;

	let mediaQuery: MediaQueryList | null = null;

	const apply = (
		nextPreference: unknown = preference,
		options: ThemeApplyOptions = {}
	): ThemeState | null => {
		preference = normalizeThemePreference(nextPreference);
		if (options.persist && storage) {
			storage.setItem(THEME_STORAGE_KEY, preference);
		}

		const state = applyThemePreference(preference, {
			animate: options.animate ?? animate,
			document: options.document ?? doc,
			prefersDark: options.prefersDark ?? prefersDark()
		});

		if (state) {
			onApply?.(state);
		}

		return state;
	};

	const handleStorage = (event: StorageEvent) => {
		if (event.key !== THEME_STORAGE_KEY) {
			return;
		}

		apply(event.newValue ?? 'system', {
			animate: true,
			persist: false
		});
	};

	const handleMediaChange = () => {
		if (preference !== 'system') {
			return;
		}

		apply('system', {
			animate: true,
			persist: false,
			prefersDark: prefersDark()
		});
	};

	if (doc) {
		apply(preference, {
			animate: false,
			persist: false,
			document: doc,
			prefersDark: prefersDark()
		});
	}

	if (typeof window !== 'undefined') {
		window.addEventListener('storage', handleStorage);
		if (typeof window.matchMedia === 'function') {
			mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
			mediaQuery.addEventListener?.('change', handleMediaChange);
		}
	}

	const destroy = () => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('storage', handleStorage);
		}

		mediaQuery?.removeEventListener?.('change', handleMediaChange);

		if (themeTransitionTimeout !== undefined && typeof window !== 'undefined') {
			window.clearTimeout(themeTransitionTimeout);
			themeTransitionTimeout = undefined;
		}
	};

	return {
		apply,
		destroy,
		get preference() {
			return preference;
		},
		get resolved() {
			return doc?.documentElement.dataset.themeResolved === 'dark' ? 'dark' : 'light';
		}
	};
}
