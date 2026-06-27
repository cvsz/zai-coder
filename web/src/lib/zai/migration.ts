import manifestData from './migration-manifest.json';

export type MigrationStatus = 'shipped' | 'integrating' | 'gap' | 'blocked';
export type MigrationPriority = 'P0' | 'P1' | 'P2';
export type MigrationRisk = 'low' | 'medium' | 'high' | 'critical';

export type QualityGate = {
	name: string;
	command: string;
	status: 'required' | 'optional';
	scope: string;
};

export type MigrationFeature = {
	name: string;
	status: MigrationStatus;
	files: string[];
	usedBy: string[];
};

export type MigrationEpic = {
	id: string;
	title: string;
	domain: string;
	status: MigrationStatus;
	priority: MigrationPriority;
	risk: MigrationRisk;
	coveragePercent: number;
	files: string[];
	dependencies: string[];
	features: MigrationFeature[];
};

export type OpenGap = {
	id: string;
	area: string;
	severity: MigrationRisk;
	status: MigrationStatus;
	target: string;
	evidence: string;
	remediation: string;
};

export type MigrationManifest = {
	version: string;
	updatedAt: string;
	releaseState: {
		name: string;
		primarySurface: string;
		baseline: string;
		localReleaseReady: boolean;
		externalGoLiveReady: boolean;
		coveragePercent: number;
		summary: string;
	};
	qualityGates: QualityGate[];
	epics: MigrationEpic[];
	openGaps: OpenGap[];
};

export type MigrationMetrics = {
	totalEpics: number;
	totalFeatures: number;
	shippedEpics: number;
	integratingEpics: number;
	gapEpics: number;
	blockedEpics: number;
	requiredGates: number;
	openBlockers: number;
	coveragePercent: number;
};

export const manifest = manifestData as unknown as MigrationManifest;

export const statusLabels: Record<MigrationStatus, string> = {
	shipped: 'Shipped',
	integrating: 'Integrating',
	gap: 'Gap',
	blocked: 'Blocked'
};

export const statusTone: Record<MigrationStatus, string> = {
	shipped: 'text-emerald-700 bg-emerald-50 border-emerald-200 dark:text-emerald-200 dark:bg-emerald-950/40 dark:border-emerald-800',
	integrating: 'text-sky-700 bg-sky-50 border-sky-200 dark:text-sky-200 dark:bg-sky-950/40 dark:border-sky-800',
	gap: 'text-amber-700 bg-amber-50 border-amber-200 dark:text-amber-200 dark:bg-amber-950/40 dark:border-amber-800',
	blocked: 'text-rose-700 bg-rose-50 border-rose-200 dark:text-rose-200 dark:bg-rose-950/40 dark:border-rose-800'
};

export const riskTone: Record<MigrationRisk, string> = {
	low: 'text-emerald-700 dark:text-emerald-300',
	medium: 'text-sky-700 dark:text-sky-300',
	high: 'text-amber-700 dark:text-amber-300',
	critical: 'text-rose-700 dark:text-rose-300'
};

export const getMigrationMetrics = (source: MigrationManifest = manifest): MigrationMetrics => {
	const byStatus = source.epics.reduce(
		(acc, epic) => {
			acc[epic.status] += 1;
			return acc;
		},
		{ shipped: 0, integrating: 0, gap: 0, blocked: 0 } satisfies Record<MigrationStatus, number>
	);

	return {
		totalEpics: source.epics.length,
		totalFeatures: source.epics.reduce((sum, epic) => sum + epic.features.length, 0),
		shippedEpics: byStatus.shipped,
		integratingEpics: byStatus.integrating,
		gapEpics: byStatus.gap,
		blockedEpics: byStatus.blocked,
		requiredGates: source.qualityGates.filter((gate) => gate.status === 'required').length,
		openBlockers: source.openGaps.filter((gap) => gap.status === 'blocked').length,
		coveragePercent: source.releaseState.coveragePercent
	};
};

export const getGoLiveBlockers = (source: MigrationManifest = manifest): OpenGap[] =>
	source.openGaps.filter((gap) => gap.status === 'blocked');

export const filterEpics = (
	source: MigrationManifest,
	status: MigrationStatus | 'all',
	query: string
): MigrationEpic[] => {
	const normalized = query.trim().toLowerCase();

	return source.epics.filter((epic) => {
		const statusMatches = status === 'all' || epic.status === status;
		if (!statusMatches) return false;
		if (!normalized) return true;

		const haystack = [
			epic.title,
			epic.domain,
			epic.status,
			epic.priority,
			epic.risk,
			...epic.files,
			...epic.dependencies,
			...epic.features.map((feature) => feature.name)
		]
			.join(' ')
			.toLowerCase();

		return haystack.includes(normalized);
	});
};
