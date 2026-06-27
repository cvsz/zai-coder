<script lang="ts">
	import Self from './OpenUIRenderer.svelte';
	import { createEventDispatcher } from 'svelte';
	import type { OpenUINode, OpenUITone } from '$lib/zai/openui';

	export let node: OpenUINode;
	export let selectedNodeId = '';

	const dispatch = createEventDispatcher<{ inspect: OpenUINode }>();

	const inspect = () => {
		dispatch('inspect', node);
	};

	const toneClass = (tone: OpenUITone = 'neutral') => {
		const tones: Record<OpenUITone, string> = {
			neutral:
				'border-gray-200 bg-white text-gray-900 dark:border-gray-800 dark:bg-gray-950 dark:text-gray-100',
			success:
				'border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-100',
			info: 'border-sky-200 bg-sky-50 text-sky-900 dark:border-sky-800 dark:bg-sky-950/40 dark:text-sky-100',
			warning:
				'border-amber-200 bg-amber-50 text-amber-900 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-100',
			danger:
				'border-rose-200 bg-rose-50 text-rose-900 dark:border-rose-800 dark:bg-rose-950/40 dark:text-rose-100'
		};

		return tones[tone];
	};

	const nodeFrameClass = () =>
		selectedNodeId === node.id
			? 'ring-2 ring-sky-400 ring-offset-2 ring-offset-white dark:ring-offset-gray-950'
			: '';
</script>

{#if node.type === 'surface'}
	<section
		class="rounded-[1.75rem] border border-gray-200 bg-gray-50/80 p-4 shadow-sm dark:border-gray-800 dark:bg-gray-950/60 md:p-5 {nodeFrameClass()}"
		aria-labelledby="{node.id}-title"
	>
		<button type="button" class="block w-full text-left" on:click={inspect}>
			<div class="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
				<div>
					<h2 id="{node.id}-title" class="text-lg font-semibold text-gray-950 dark:text-gray-50">
						{node.title}
					</h2>
					{#if node.description}
						<p class="mt-1 max-w-3xl text-sm leading-6 text-gray-600 dark:text-gray-300">
							{node.description}
						</p>
					{/if}
				</div>
				<span
					class="w-fit rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-600 dark:border-gray-800 dark:bg-gray-900 dark:text-gray-300"
				>
					{node.type}
				</span>
			</div>
		</button>

		<div class="mt-5 space-y-4">
			{#each node.children ?? [] as child (child.id)}
				<Self
					node={child}
					{selectedNodeId}
					on:inspect={(event) => dispatch('inspect', event.detail)}
				/>
			{/each}
		</div>
	</section>
{:else if node.type === 'grid'}
	<section
		class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900/80 {nodeFrameClass()}"
		aria-labelledby="{node.id}-title"
	>
		<button type="button" class="mb-3 flex w-full items-center justify-between text-left" on:click={inspect}>
			<h3 id="{node.id}-title" class="text-sm font-semibold text-gray-950 dark:text-gray-50">
				{node.title}
			</h3>
			<span class="text-xs font-medium text-gray-500 dark:text-gray-400">{node.type}</span>
		</button>
		<div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
			{#each node.children ?? [] as child (child.id)}
				<Self
					node={child}
					{selectedNodeId}
					on:inspect={(event) => dispatch('inspect', event.detail)}
				/>
			{/each}
		</div>
	</section>
{:else if node.type === 'panel'}
	<section
		class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900/80 {nodeFrameClass()}"
		aria-labelledby="{node.id}-title"
	>
		<button type="button" class="block w-full text-left" on:click={inspect}>
			<h3 id="{node.id}-title" class="text-sm font-semibold text-gray-950 dark:text-gray-50">
				{node.title}
			</h3>
			{#if node.description}
				<p class="mt-1 text-sm leading-6 text-gray-600 dark:text-gray-300">{node.description}</p>
			{/if}
		</button>
		<div class="mt-3 grid gap-3 md:grid-cols-2">
			{#each node.children ?? [] as child (child.id)}
				<Self
					node={child}
					{selectedNodeId}
					on:inspect={(event) => dispatch('inspect', event.detail)}
				/>
			{/each}
		</div>
	</section>
{:else if node.type === 'metric'}
	<button
		type="button"
		class="rounded-2xl border p-4 text-left transition hover:-translate-y-0.5 hover:shadow-md {toneClass(node.tone)} {nodeFrameClass()}"
		on:click={inspect}
	>
		<div class="text-xs font-medium uppercase tracking-[0.18em] opacity-70">{node.label}</div>
		<div class="mt-3 text-3xl font-semibold tracking-normal">{node.value}</div>
	</button>
{:else if node.type === 'status'}
	<button
		type="button"
		class="flex items-center justify-between gap-3 rounded-2xl border px-4 py-3 text-left transition hover:shadow-sm {toneClass(node.tone)} {nodeFrameClass()}"
		on:click={inspect}
	>
		<span class="text-sm font-medium">{node.label}</span>
		<span class="rounded-full bg-white/60 px-2.5 py-1 text-xs font-semibold dark:bg-black/20">
			{node.value}
		</span>
	</button>
{:else if node.type === 'list'}
	<section
		class="rounded-3xl border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-800 dark:bg-gray-900/80 {nodeFrameClass()}"
		aria-labelledby="{node.id}-title"
	>
		<button type="button" class="mb-3 flex w-full items-center justify-between text-left" on:click={inspect}>
			<h3 id="{node.id}-title" class="text-sm font-semibold text-gray-950 dark:text-gray-50">
				{node.title}
			</h3>
			<span class="text-xs font-medium text-gray-500 dark:text-gray-400">{node.type}</span>
		</button>
		<div class="space-y-2">
			{#each node.items ?? [] as item}
				<div class="rounded-2xl border px-3 py-2 {toneClass(item.tone)}">
					<div class="text-sm font-semibold">{item.label}</div>
					{#if item.value}
						<div class="mt-1 text-xs leading-5 opacity-80">{item.value}</div>
					{/if}
				</div>
			{/each}
		</div>
	</section>
{:else if node.type === 'action'}
	<a
		class="inline-flex items-center justify-center rounded-2xl border border-gray-900 bg-gray-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-gray-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 dark:border-gray-100 dark:bg-gray-100 dark:text-gray-950 dark:hover:bg-white {nodeFrameClass()}"
		href={node.href}
		on:click={inspect}
	>
		{node.label}
	</a>
{:else if node.type === 'code'}
	<button
		type="button"
		class="block w-full rounded-3xl border border-gray-200 bg-gray-950 p-4 text-left text-gray-100 shadow-sm {nodeFrameClass()}"
		on:click={inspect}
	>
		<div class="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-gray-400">{node.title}</div>
		<pre class="max-h-80 overflow-auto whitespace-pre-wrap text-xs leading-5">{node.source}</pre>
	</button>
{:else if node.type === 'remote'}
	<button
		type="button"
		class="block w-full rounded-3xl border border-dashed border-sky-300 bg-sky-50/70 p-4 text-left shadow-sm transition hover:bg-sky-50 dark:border-sky-800 dark:bg-sky-950/30 dark:hover:bg-sky-950/50 {nodeFrameClass()}"
		on:click={inspect}
	>
		<div class="flex flex-col gap-2 md:flex-row md:items-start md:justify-between">
			<div>
				<h3 class="text-sm font-semibold text-sky-950 dark:text-sky-100">{node.title}</h3>
				{#if node.description}
					<p class="mt-1 text-sm leading-6 text-sky-800 dark:text-sky-200">{node.description}</p>
				{/if}
			</div>
			<span class="rounded-full bg-white px-3 py-1 text-xs font-semibold text-sky-700 dark:bg-gray-950 dark:text-sky-200">
				remote
			</span>
		</div>
		{#if node.source}
			<code
				class="mt-3 block overflow-auto rounded-2xl bg-white px-3 py-2 text-xs text-sky-900 dark:bg-gray-950 dark:text-sky-100"
			>
				{node.source}
			</code>
		{/if}
	</button>
{/if}
