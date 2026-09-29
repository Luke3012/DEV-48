from __future__ import annotations

from pathlib import Path

from .models import Lab
from .amazon_mock_scaffolds import parcel_cpp_repository, parcel_node_repository


def ensure_amazon_repo_scaffold(target: Path, lab: Lab) -> None:
    """Create a deliberately imperfect, multi-file repository for OA practice."""
    files = _repositories().get(lab.id)
    if files is None:
        raise ValueError(f"Repository Amazon sconosciuta: {lab.id}")
    for relative, content in files.items():
        path = target / relative
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _repositories() -> dict[str, dict[str, str]]:
    cpp_demo = {
        "CMakeLists.txt": "cmake_minimum_required(VERSION 3.16)\nproject(subject_catalog LANGUAGES CXX)\nset(CMAKE_CXX_STANDARD 20)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\n",
        "include/subject_catalog.h": '''#pragma once
#include <optional>
#include <string>
#include <vector>

struct Subject {
    int id;
    std::string name;
    bool active;
};

std::vector<Subject> visible_active(const std::vector<Subject>& subjects);
std::optional<Subject> find_subject(const std::vector<Subject>& subjects, int id);
''',
        "src/subject_catalog.cpp": '''#include "subject_catalog.h"

std::vector<Subject> visible_active(const std::vector<Subject>& subjects) {
    std::vector<Subject> visible;
    for (const auto& subject : subjects) {
        if (!subject.active) visible.push_back(subject);
    }
    return visible;
}

std::optional<Subject> find_subject(const std::vector<Subject>& subjects, int id) {
    for (const auto& subject : subjects) {
        if (subject.id >= id) return subject;
    }
    return std::nullopt;
}
''',
        "tests/test_main.cpp": '''#include "subject_catalog.h"
#include <iostream>

int main() {
    int failed = 0;
    const std::vector<Subject> subjects{{1, "Ari", true}, {2, "Bea", false}, {3, "Ciro", true}};
    auto check = [&](bool ok, const char* name) {
        std::cout << (ok ? "PASS " : "FAIL ") << name << "\\n";
        failed += !ok;
    };
    const auto visible = visible_active(subjects);
    check(visible.size() == 2 && visible[0].id == 1 && visible[1].id == 3, "mantiene solo i soggetti attivi");
    const auto found = find_subject(subjects, 2);
    check(found && found->name == "Bea", "trova l'identificativo esatto");
    check(!find_subject(subjects, 0), "non restituisce un ID maggiore al posto di quello assente");
    check(!find_subject(subjects, 9), "restituisce vuoto quando l'ID manca");
    return failed ? 1 : 0;
}
''',
    }
    node_demo = {
        "package.json": '''{"private":true,"type":"module","scripts":{"test":"node --test"}}\n''',
        "src/subjectService.js": '''export function visibleActive(subjects) {
  return subjects.filter(subject => !subject.active);
}

export function findSubject(subjects, id) {
  return subjects.find(subject => subject.id >= id) ?? null;
}
''',
        "test/subjectService.test.js": '''import test from 'node:test';
import assert from 'node:assert/strict';
import { findSubject, visibleActive } from '../src/subjectService.js';

const subjects = [
  { id: 1, name: 'Ari', active: true },
  { id: 2, name: 'Bea', active: false },
  { id: 3, name: 'Ciro', active: true },
];

test('mostra soltanto i soggetti attivi', () => {
  assert.deepEqual(visibleActive(subjects).map(subject => subject.id), [1, 3]);
});

test('trova l’identificativo esatto e gestisce quello assente', () => {
  assert.equal(findSubject(subjects, 2)?.name, 'Bea');
  assert.equal(findSubject(subjects, 0), null);
  assert.equal(findSubject(subjects, 9), null);
});

test('la ricerca non modifica il dataset', () => {
  const snapshot = structuredClone(subjects);
  visibleActive(subjects);
  assert.deepEqual(subjects, snapshot);
});
''',
    }
    node_async = {
        "package.json": '''{"private":true,"type":"module","scripts":{"test":"node --test"}}\n''',
        "src/profileRepository.js": '''const profiles = new Map([
  ['17', { id: '17', name: 'Ada', active: true }],
  ['18', { id: '18', name: 'Nico', active: false }],
]);

export async function readProfile(id) {
  return profiles.get(String(id)) ?? null;
}
''',
        "src/profileController.js": '''import { readProfile } from './profileRepository.js';

export async function getProfile(id) {
  const profile = readProfile(id);
  if (!profile) return { status: 404, body: { error: 'not found' } };
  return { status: 200, body: profile };
}
''',
        "test/profileController.test.js": '''import test from 'node:test';
import assert from 'node:assert/strict';
import { getProfile } from '../src/profileController.js';

test('restituisce il profilo dopo il caricamento asincrono', async () => {
  const response = await getProfile('17');
  assert.equal(response.status, 200);
  assert.equal(response.body.name, 'Ada');
});

test('un profilo mancante produce 404', async () => {
  const response = await getProfile('999');
  assert.equal(response.status, 404);
  assert.deepEqual(response.body, { error: 'not found' });
});
''',
    }
    cpp_inventory = {
        "CMakeLists.txt": "cmake_minimum_required(VERSION 3.16)\nproject(inventory LANGUAGES CXX)\nset(CMAKE_CXX_STANDARD 20)\nset(CMAKE_CXX_STANDARD_REQUIRED ON)\n",
        "include/inventory.h": '''#pragma once
#include <optional>
#include <string>
#include <vector>

struct Item { int id; std::string name; int quantity; };
bool remove_item(std::vector<Item>& items, std::size_t index);
std::optional<Item> find_item(const std::vector<Item>& items, int id);
''',
        "src/inventory.cpp": '''#include "inventory.h"

bool remove_item(std::vector<Item>& items, std::size_t index) {
    if (index > items.size()) return false;
    items.erase(items.begin() + static_cast<std::ptrdiff_t>(index));
    return true;
}

std::optional<Item> find_item(const std::vector<Item>& items, int id) {
    for (const auto& item : items) {
        if (item.id >= id) return item;
    }
    return std::nullopt;
}
''',
        "src/stock_service.cpp": '''#include "inventory.h"

int total_units(const std::vector<Item>& items) {
    int total = 0;
    for (const auto& item : items) total += item.quantity;
    return total;
}
''',
        "include/stock_service.h": '''#pragma once
#include "inventory.h"
int total_units(const std::vector<Item>& items);
''',
        "tests/test_main.cpp": '''#include "inventory.h"
#include "stock_service.h"
#include <iostream>

int main() {
    int failed = 0;
    auto check = [&](bool ok, const char* name) {
        std::cout << (ok ? "PASS " : "FAIL ") << name << "\\n";
        failed += !ok;
    };
    std::vector<Item> items{{4, "cavo", 3}, {9, "adattatore", 0}};
    check(total_units(items) == 3, "le unità nulle non cambiano la somma");
    check(find_item(items, 9)->name == "adattatore", "lookup per ID esatto");
    auto last = items;
    check(remove_item(last, 1) && last.size() == 1, "rimuove l'ultimo indice valido");
    check(!find_item(items, 7), "un ID assente intermedio non restituisce un altro articolo");
    check(!remove_item(items, 2) && items.size() == 2, "rifiuta l'indice uguale alla dimensione");
    return failed ? 1 : 0;
}
''',
    }
    node_contract = {
        "package.json": '''{"private":true,"type":"module","scripts":{"test":"node --test"}}\n''',
        "src/orderService.js": '''export function summarizeOrder(order) {
  const lines = order.lines || [];
  const total = lines.reduce((sum, line) => sum + line.price * line.quantity, 0);
  return { orderId: order.id, total, itemCount: lines.length };
}

export function visibleOrders(orders, status) {
  return orders.sort((a, b) => a.createdAt.localeCompare(b.createdAt))
    .filter(order => !status || order.status !== status);
}

export function findOrder(orders, orderId) {
  return orders.find(order => order.id === orderId) || {};
}
''',
        "src/orderController.js": '''import { findOrder, summarizeOrder } from './orderService.js';

export function getOrder(orders, id) {
  const order = findOrder(orders, id);
  if (!order) return { status: 404, body: { error: 'not found' } };
  return { status: 200, body: summarizeOrder(order) };
}
''',
        "test/orderService.test.js": '''import test from 'node:test';
import assert from 'node:assert/strict';
import { getOrder } from '../src/orderController.js';
import { summarizeOrder, visibleOrders } from '../src/orderService.js';

test('somma le righe e conserva il numero degli articoli', () => {
  assert.deepEqual(summarizeOrder({ id: 'o1', lines: [{ price: 3, quantity: 2 }] }),
    { orderId: 'o1', total: 6, itemCount: 1 });
});

test('filtra per stato senza riordinare o mutare l’input', () => {
  const orders = [{ id: 'b', status: 'open', createdAt: '2026-02' }, { id: 'a', status: 'closed', createdAt: '2026-01' }];
  const snapshot = structuredClone(orders);
  assert.deepEqual(visibleOrders(orders, 'open').map(order => order.id), ['b']);
  assert.deepEqual(orders, snapshot);
});

test('un ordine inesistente restituisce un 404 esplicito', () => {
  assert.deepEqual(getOrder([], 'missing'), { status: 404, body: { error: 'not found' } });
});
''',
    }
    return {
        "lab-amazon-cpp-demo": cpp_demo,
        "lab-amazon-node-demo": node_demo,
        "lab-amazon-node-async": node_async,
        "lab-amazon-cpp-inventory": cpp_inventory,
        "lab-amazon-node-contract": node_contract,
        "lab-amazon-mock-repository": parcel_node_repository(),
        "lab-amazon-mock-repository-cpp": parcel_cpp_repository(),
    }
