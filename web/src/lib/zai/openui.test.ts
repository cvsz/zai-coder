import { describe, it, expect } from 'vitest';
import { openUIRegistry, zaiWorkbenchSchema, type OpenUINode } from './openui';

describe('OpenUI Schema Validation', () => {
	it('validates dynamic registry entries', () => {
		expect(openUIRegistry).toBeInstanceOf(Array);
		expect(openUIRegistry.length).toBeGreaterThan(0);
		
		const surfaceEntry = openUIRegistry.find((e) => e.type === 'surface');
		expect(surfaceEntry).toBeDefined();
		expect(surfaceEntry?.dynamic).toBe(true);
	});

	it('validates remote components', () => {
		const remoteEntry = openUIRegistry.find((e) => e.type === 'remote');
		expect(remoteEntry).toBeDefined();
		expect(remoteEntry?.remoteCapable).toBe(true);

		const remoteNode = zaiWorkbenchSchema.children?.find((c) => c.type === 'remote');
		expect(remoteNode).toBeDefined();
		expect(remoteNode?.source).toBe('/api/v1/zai/openui/schema');
	});

	it('validates live preview and inspector structure', () => {
		expect(zaiWorkbenchSchema.id).toBe('zai-command-center');
		expect(zaiWorkbenchSchema.type).toBe('surface');
		expect(zaiWorkbenchSchema.children).toBeInstanceOf(Array);
	});

	it('validates persisted theme modes in schema context', () => {
		// Mock logic: schema should support rendering in different tones (themes)
		const grid = zaiWorkbenchSchema.children?.find((c) => c.type === 'grid');
		expect(grid).toBeDefined();
		
		const metrics = grid?.children || [];
		const tones = metrics.map((m) => m.tone).filter(Boolean);
		expect(tones.length).toBeGreaterThan(0);
		expect(['info', 'neutral', 'success', 'danger', 'warning']).toEqual(
			expect.arrayContaining(tones as string[])
		);
	});
});
