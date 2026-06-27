import { getGoLiveBlockers, getMigrationMetrics, manifest } from './migration';

export type OpenUITone = 'neutral' | 'success' | 'info' | 'warning' | 'danger';
export type OpenUINodeType =
	| 'surface'
	| 'panel'
	| 'grid'
	| 'metric'
	| 'status'
	| 'list'
	| 'action'
	| 'code'
	| 'remote';

export type OpenUIListItem = {
	label: string;
	value?: string;
	tone?: OpenUITone;
};

export type OpenUINode = {
	id: string;
	type: OpenUINodeType;
	title?: string;
	description?: string;
	label?: string;
	value?: string | number;
	tone?: OpenUITone;
	href?: string;
	source?: string;
	items?: OpenUIListItem[];
	children?: OpenUINode[];
};

export type OpenUIRegistryEntry = {
	type: OpenUINodeType;
	label: string;
	description: string;
	dynamic: boolean;
	remoteCapable: boolean;
};

const metrics = getMigrationMetrics();
const blockers = getGoLiveBlockers();

export const openUIRegistry: OpenUIRegistryEntry[] = [
	{
		type: 'surface',
		label: 'Surface',
		description: 'Top-level OpenUI document node.',
		dynamic: true,
		remoteCapable: false
	},
	{
		type: 'panel',
		label: 'Panel',
		description: 'Section container with heading and optional children.',
		dynamic: true,
		remoteCapable: false
	},
	{
		type: 'grid',
		label: 'Grid',
		description: 'Responsive layout for repeated metrics or cards.',
		dynamic: true,
		remoteCapable: false
	},
	{
		type: 'metric',
		label: 'Metric',
		description: 'Compact numeric or state summary.',
		dynamic: true,
		remoteCapable: true
	},
	{
		type: 'status',
		label: 'Status',
		description: 'Readiness or risk state with semantic color.',
		dynamic: true,
		remoteCapable: true
	},
	{
		type: 'list',
		label: 'List',
		description: 'Structured list of records with optional tones.',
		dynamic: true,
		remoteCapable: true
	},
	{
		type: 'action',
		label: 'Action',
		description: 'Navigation or command link rendered as a control.',
		dynamic: true,
		remoteCapable: true
	},
	{
		type: 'code',
		label: 'Code',
		description: 'Read-only schema or command payload viewer.',
		dynamic: true,
		remoteCapable: true
	},
	{
		type: 'remote',
		label: 'Remote',
		description: 'Remote component contract rendered as a safe inspectable endpoint.',
		dynamic: true,
		remoteCapable: true
	}
];

export const zaiWorkbenchSchema: OpenUINode = {
	id: 'zai-command-center',
	type: 'surface',
	title: 'ZAI Coder Command Center',
	description: manifest.releaseState.summary,
	children: [
		{
			id: 'release-metrics',
			type: 'grid',
			title: 'Release Metrics',
			children: [
				{
					id: 'coverage',
					type: 'metric',
					label: 'Coverage',
					value: `${metrics.coveragePercent}%`,
					tone: 'info'
				},
				{
					id: 'epics',
					type: 'metric',
					label: 'Epics',
					value: metrics.totalEpics,
					tone: 'neutral'
				},
				{
					id: 'required-gates',
					type: 'metric',
					label: 'Required Gates',
					value: metrics.requiredGates,
					tone: 'success'
				},
				{
					id: 'go-live-blockers',
					type: 'metric',
					label: 'Go-Live Blockers',
					value: metrics.openBlockers,
					tone: metrics.openBlockers > 0 ? 'danger' : 'success'
				}
			]
		},
		{
			id: 'go-live-state',
			type: 'panel',
			title: 'Go-Live State',
			description: manifest.releaseState.externalGoLiveReady
				? 'External go-live gate is open.'
				: 'External go-live remains blocked by production hardening gates.',
			children: [
				{
					id: 'local-release',
					type: 'status',
					label: 'Local release',
					value: manifest.releaseState.localReleaseReady ? 'Ready' : 'Blocked',
					tone: manifest.releaseState.localReleaseReady ? 'success' : 'danger'
				},
				{
					id: 'external-release',
					type: 'status',
					label: 'External service',
					value: manifest.releaseState.externalGoLiveReady ? 'Ready' : 'Blocked',
					tone: manifest.releaseState.externalGoLiveReady ? 'success' : 'danger'
				}
			]
		},
		{
			id: 'blocker-list',
			type: 'list',
			title: 'Critical Blockers',
			items: blockers.map((gap) => ({
				label: gap.area,
				value: `${gap.target}: ${gap.remediation}`,
				tone: gap.severity === 'critical' ? 'danger' : 'warning'
			}))
		},
		{
			id: 'remote-contract',
			type: 'remote',
			title: 'Remote Component Contract',
			description:
				'Remote components are accepted only as JSON schema documents that pass registry validation before rendering.',
			source: '/api/v1/zai/openui/schema'
		}
	]
};
