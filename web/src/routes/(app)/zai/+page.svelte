<script lang="ts">
	import OpenUIRenderer from '$lib/components/zai/OpenUIRenderer.svelte';
	import Code from '$lib/components/icons/Code.svelte';
	import CommandLine from '$lib/components/icons/CommandLine.svelte';
	import Database from '$lib/components/icons/Database.svelte';
	import Sparkles from '$lib/components/icons/Sparkles.svelte';
	import {
		filterEpics,
		getGoLiveBlockers,
		getMigrationMetrics,
		manifest,
		riskTone,
		statusLabels,
		statusTone,
		type MigrationEpic,
		type MigrationStatus
	} from '$lib/zai/migration';
	import { openUIRegistry, zaiWorkbenchSchema, type OpenUINode } from '$lib/zai/openui';

	type StatusFilter = MigrationStatus | 'all';

	const statusFilters: Array<{ value: StatusFilter; label: string }> = [
		{ value: 'all', label: 'All' },
		{ value: 'shipped', label: 'Shipped' },
		{ value: 'integrating', label: 'Integrating' },
		{ value: 'gap', label: 'Gaps' },
		{ value: 'blocked', label: 'Blocked' }
	];
	const devtools = ['canvas', 'schema', 'registry'] as const;

	let statusFilter: StatusFilter = 'all';
	let query = '';
	let selectedNode: OpenUINode = zaiWorkbenchSchema;
	let activeDevtool: 'canvas' | 'schema' | 'registry' = 'canvas';

	$: metrics = getMigrationMetrics();
	$: blockers = getGoLiveBlockers();
	$: filteredEpics = filterEpics(manifest, statusFilter, query);
	$: selectedSchema = JSON.stringify(selectedNode, null, 2);
	$: fullSchema = JSON.stringify(zaiWorkbenchSchema, null, 2);

	const inspectNode = (node: OpenUINode) => {
		selectedNode = node;
		activeDevtool = 'canvas';
	};

	const epicProgressLabel = (epic: MigrationEpic) =>
		`${epic.coveragePercent}% coverage, ${epic.features.length} tracked features`;
</script>

<svelte:head>
	<title>ZAI Command Center</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 text-gray-950 dark:bg-gray-950 dark:text-gray-50">
	<div class="mx-auto flex w-full max-w-[1640px] flex-col gap-6 px-4 py-4 md:px-6 lg:px-8">
		<header class="rounded-[2rem] border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-gray-900">
			<div class="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
				<div class="max-w-4xl">
					<div class="flex items-center gap-3 text-sm font-semibold text-sky-700 dark:text-sky-300">
						<span
							class="inline-flex size-9 items-center justify-center rounded-2xl bg-sky-100 text-sky-800 dark:bg-sky-950 dark:text-sky-200"
						>
							<Sparkles className="size-4.5" strokeWidth="2" />
						</span>
						<span>ZAI UX/UI</span>
					</div>
					<h1 class="mt-4 text-3xl font-semibold tracking-normal text-gray-950 dark:text-gray-50 md:text-5xl">
						ZAI Coder Command Center
					</h1>
					<p class="mt-4 max-w-3xl text-sm leading-6 text-gray-600 dark:text-gray-300 md:text-base">
						{manifest.releaseState.summary}
					</p>
				</div>

				<div class="grid gap-3 sm:grid-cols-2 xl:min-w-[520px]">
					<div class="rounded-3xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-950">
						<div class="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500 dark:text-gray-400">
							Primary surface
						</div>
						<div class="mt-3 text-2xl font-semibold">{manifest.releaseState.primarySurface}</div>
						<div class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400">
							{manifest.releaseState.baseline}
						</div>
					</div>
					<div class="rounded-3xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-950">
						<div class="text-xs font-semibold uppercase tracking-[0.18em] text-gray-500 dark:text-gray-400">
							Go-live
						</div>
						<div class="mt-3 text-2xl font-semibold">
							{manifest.releaseState.externalGoLiveReady ? 'Ready' : 'Blocked'}
						</div>
						<div class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400">
							{blockers.length} critical blockers remain in the release gate.
						</div>
					</div>
				</div>
			</div>
		</header>

		<section class="grid gap-4 md:grid-cols-2 xl:grid-cols-4" aria-label="Migration summary">
			<div class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
				<div class="flex items-center gap-3 text-sm font-semibold text-gray-600 dark:text-gray-300">
					<Code className="size-4.5" strokeWidth="2" />
					<span>Coverage</span>
				</div>
				<div class="mt-4 text-4xl font-semibold">{metrics.coveragePercent}%</div>
				<progress
					class="mt-3 h-2 w-full overflow-hidden rounded-full accent-sky-500"
					value={metrics.coveragePercent}
					max="100"
					aria-label="Overall migration coverage"
				></progress>
			</div>
			<div class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
				<div class="flex items-center gap-3 text-sm font-semibold text-gray-600 dark:text-gray-300">
					<CommandLine className="size-4.5" strokeWidth="2" />
					<span>Quality gates</span>
				</div>
				<div class="mt-4 text-4xl font-semibold">{metrics.requiredGates}</div>
				<div class="mt-2 text-sm text-gray-500 dark:text-gray-400">Required before release sign-off.</div>
			</div>
			<div class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
				<div class="flex items-center gap-3 text-sm font-semibold text-gray-600 dark:text-gray-300">
					<Database className="size-4.5" strokeWidth="2" />
					<span>Epics</span>
				</div>
				<div class="mt-4 text-4xl font-semibold">{metrics.totalEpics}</div>
				<div class="mt-2 text-sm text-gray-500 dark:text-gray-400">{metrics.totalFeatures} feature rows tracked.</div>
			</div>
			<div class="rounded-3xl border border-rose-200 bg-rose-50 p-4 shadow-sm dark:border-rose-900 dark:bg-rose-950/30">
				<div class="flex items-center gap-3 text-sm font-semibold text-rose-700 dark:text-rose-200">
					<Sparkles className="size-4.5" strokeWidth="2" />
					<span>Blockers</span>
				</div>
				<div class="mt-4 text-4xl font-semibold text-rose-900 dark:text-rose-50">{metrics.openBlockers}</div>
				<div class="mt-2 text-sm text-rose-700 dark:text-rose-200">External go-live cannot proceed yet.</div>
			</div>
		</section>

		<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900" aria-label="Module Control Views">
			<h2 class="text-lg font-semibold">Module Control Views</h2>
			<div class="mt-4 grid gap-3 lg:grid-cols-4 sm:grid-cols-2">
				{#each [
					{ name: 'Operations', path: '/zai/operations' },
					{ name: 'Governance', path: '/zai/governance' },
					{ name: 'Compliance', path: '/zai/compliance' },
					{ name: 'Provider Routing', path: '/zai/providers' },
					{ name: 'Marketplace', path: '/zai/marketplace' },
					{ name: 'Go-Live', path: '/zai/go-live' },
					{ name: 'Release', path: '/zai/release' },
					{ name: 'Evals', path: '/zai/evals' }
				] as view}
					<a
						href={view.path}
						class="flex items-center justify-between rounded-2xl border border-gray-200 bg-gray-50 p-3 hover:bg-gray-100 transition dark:border-gray-800 dark:bg-gray-950 dark:hover:bg-gray-900"
					>
						<span class="text-sm font-semibold">{view.name}</span>
						<span class="text-gray-400">&rarr;</span>
					</a>
				{/each}
			</div>
		</section>

		<div class="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(420px,0.8fr)]">
			<section class="space-y-5">
				<div class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
					<div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
						<div>
							<h2 class="text-lg font-semibold">Feature Migration Inventory</h2>
							<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
								Filter every tracked web migration epic by status, dependency, file path, or feature name.
							</p>
						</div>
						<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
							<label class="sr-only" for="migration-search">Search migration inventory</label>
							<input
								id="migration-search"
								class="min-h-10 rounded-2xl border border-gray-200 bg-gray-50 px-3 text-sm outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-100 dark:border-gray-800 dark:bg-gray-950 dark:focus:ring-sky-950"
								placeholder="Search features, files, dependencies"
								bind:value={query}
							/>
							<div
								class="flex flex-wrap gap-1 rounded-2xl border border-gray-200 bg-gray-50 p-1 dark:border-gray-800 dark:bg-gray-950"
								role="radiogroup"
								aria-label="Migration status filter"
							>
								{#each statusFilters as item}
									<button
										type="button"
										class="rounded-xl px-3 py-1.5 text-xs font-semibold transition {statusFilter === item.value
											? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950'
											: 'text-gray-600 hover:bg-white dark:text-gray-300 dark:hover:bg-gray-900'}"
										role="radio"
										aria-checked={statusFilter === item.value}
										on:click={() => (statusFilter = item.value)}
									>
										{item.label}
									</button>
								{/each}
							</div>
						</div>
					</div>
				</div>

				<div class="space-y-3">
					{#each filteredEpics as epic (epic.id)}
						<article class="rounded-[1.75rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
							<div class="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
								<div class="min-w-0">
									<div class="flex flex-wrap items-center gap-2">
										<span class="rounded-full border px-2.5 py-1 text-xs font-semibold {statusTone[epic.status]}">
											{statusLabels[epic.status]}
										</span>
										<span class="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-semibold text-gray-700 dark:bg-gray-800 dark:text-gray-200">
											{epic.priority}
										</span>
										<span class="text-xs font-semibold {riskTone[epic.risk]}">{epic.risk} risk</span>
									</div>
									<h3 class="mt-3 text-xl font-semibold tracking-normal">{epic.title}</h3>
									<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{epicProgressLabel(epic)}</p>
								</div>
								<div class="min-w-[180px]">
									<div class="flex items-center justify-between text-xs font-semibold text-gray-500 dark:text-gray-400">
										<span>Coverage</span>
										<span>{epic.coveragePercent}%</span>
									</div>
									<progress
										class="mt-2 h-2 w-full overflow-hidden rounded-full accent-gray-950 dark:accent-gray-100"
										value={epic.coveragePercent}
										max="100"
										aria-label="{epic.title} migration coverage"
									></progress>
								</div>
							</div>

							<div class="mt-4 grid gap-3 lg:grid-cols-3">
								<div>
									<div class="text-xs font-semibold uppercase tracking-[0.16em] text-gray-500 dark:text-gray-400">
										Files
									</div>
									<div class="mt-2 space-y-1">
										{#each epic.files as file}
											<code class="block truncate rounded-xl bg-gray-50 px-2.5 py-1.5 text-xs text-gray-700 dark:bg-gray-950 dark:text-gray-300">
												{file}
											</code>
										{/each}
									</div>
								</div>
								<div>
									<div class="text-xs font-semibold uppercase tracking-[0.16em] text-gray-500 dark:text-gray-400">
										Dependencies
									</div>
									<div class="mt-2 flex flex-wrap gap-1.5">
										{#each epic.dependencies as dependency}
											<span class="rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-700 dark:bg-gray-800 dark:text-gray-200">
												{dependency}
											</span>
										{/each}
									</div>
								</div>
								<div>
									<div class="text-xs font-semibold uppercase tracking-[0.16em] text-gray-500 dark:text-gray-400">
										Feature rows
									</div>
									<div class="mt-2 space-y-2">
										{#each epic.features as feature}
											<div class="rounded-2xl border border-gray-200 p-2 dark:border-gray-800">
												<div class="flex items-center justify-between gap-2">
													<span class="text-sm font-medium">{feature.name}</span>
													<span class="rounded-full border px-2 py-0.5 text-[11px] font-semibold {statusTone[feature.status]}">
														{statusLabels[feature.status]}
													</span>
												</div>
												<div class="mt-1 text-xs text-gray-500 dark:text-gray-400">
													Used by {feature.usedBy.join(', ')}
												</div>
											</div>
										{/each}
									</div>
								</div>
							</div>
						</article>
					{/each}
				</div>
			</section>

			<aside class="space-y-5">
				<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
					<div class="flex items-center justify-between gap-3">
						<div>
							<h2 class="text-lg font-semibold">OpenUI Devtools</h2>
							<p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
								Inspect the live schema, registry, and selected node.
							</p>
						</div>
						<div class="flex rounded-2xl border border-gray-200 bg-gray-50 p-1 dark:border-gray-800 dark:bg-gray-950">
							{#each devtools as tool}
								<button
									type="button"
									class="rounded-xl px-2.5 py-1.5 text-xs font-semibold capitalize transition {activeDevtool === tool
										? 'bg-gray-950 text-white dark:bg-white dark:text-gray-950'
										: 'text-gray-600 hover:bg-white dark:text-gray-300 dark:hover:bg-gray-900'}"
									on:click={() => (activeDevtool = tool)}
								>
									{tool}
								</button>
							{/each}
						</div>
					</div>
				</section>

				{#if activeDevtool === 'canvas'}
					<OpenUIRenderer
						node={zaiWorkbenchSchema}
						selectedNodeId={selectedNode.id}
						on:inspect={(event) => inspectNode(event.detail)}
					/>
					<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
						<h3 class="text-sm font-semibold">Inspector</h3>
						<p class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400">
							Selected node: <code>{selectedNode.id}</code>
						</p>
						<pre class="mt-3 max-h-80 overflow-auto rounded-2xl bg-gray-950 p-3 text-xs leading-5 text-gray-100">{selectedSchema}</pre>
					</section>
				{:else if activeDevtool === 'schema'}
					<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
						<h3 class="text-sm font-semibold">JSON UI Schema</h3>
						<pre class="mt-3 max-h-[720px] overflow-auto rounded-2xl bg-gray-950 p-3 text-xs leading-5 text-gray-100">{fullSchema}</pre>
					</section>
				{:else}
					<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
						<h3 class="text-sm font-semibold">Component Registry</h3>
						<div class="mt-3 space-y-2">
							{#each openUIRegistry as entry}
								<div class="rounded-2xl border border-gray-200 p-3 dark:border-gray-800">
									<div class="flex items-center justify-between gap-3">
										<div class="font-semibold">{entry.label}</div>
										<div class="rounded-full bg-gray-100 px-2.5 py-1 text-xs dark:bg-gray-800">
											{entry.type}
										</div>
									</div>
									<p class="mt-1 text-xs leading-5 text-gray-500 dark:text-gray-400">{entry.description}</p>
									<div class="mt-2 flex flex-wrap gap-1.5 text-[11px] font-semibold">
										<span class="rounded-full bg-emerald-50 px-2 py-1 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-200">
											{entry.dynamic ? 'dynamic' : 'static'}
										</span>
										<span class="rounded-full bg-sky-50 px-2 py-1 text-sky-700 dark:bg-sky-950 dark:text-sky-200">
											{entry.remoteCapable ? 'remote-capable' : 'local'}
										</span>
									</div>
								</div>
							{/each}
						</div>
					</section>
				{/if}
			</aside>
		</div>

		<section class="rounded-[2rem] border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900">
			<h2 class="text-lg font-semibold">Required Release Gates</h2>
			<div class="mt-4 grid gap-3 lg:grid-cols-2">
				{#each manifest.qualityGates as gate}
					<div class="rounded-2xl border border-gray-200 bg-gray-50 p-3 dark:border-gray-800 dark:bg-gray-950">
						<div class="flex flex-wrap items-center justify-between gap-2">
							<div class="text-sm font-semibold">{gate.name}</div>
							<span class="rounded-full bg-white px-2.5 py-1 text-xs font-semibold text-gray-600 dark:bg-gray-900 dark:text-gray-300">
								{gate.scope}
							</span>
						</div>
						<code class="mt-2 block overflow-auto rounded-xl bg-white px-3 py-2 text-xs text-gray-700 dark:bg-gray-900 dark:text-gray-200">
							{gate.command}
						</code>
					</div>
				{/each}
			</div>
		</section>
	</div>
</div>
