"""Acceptance-driven parcel repositories for the final timed assessment.

These are teaching starters, deliberately containing defects. They have no network
dependencies and do not contain the reference repairs.
"""


def parcel_node_repository() -> dict[str, str]:
    return {
        "package.json": '{"private":true,"type":"module","scripts":{"test":"node --test"}}\n',
        "README.md": """# Parcel status service

Run `npm test`. The API lists parcels belonging to a customer, optionally matching
a status, and returns a detail summary. Reads must preserve stored records.

Transitions are ready -> in_transit -> delivered. A missing parcel returns 404;
an invalid transition returns 409 and changes nothing. Each successful transition
adds one status event. A requestId is an idempotency key **for one parcel**: retrying
that request returns its original response without another event. Different parcels
may use the same requestId. A retry with a different target status returns 409.

Return response bodies as snapshots: later operations must not change an earlier
response. Existing API names and signatures are the compatibility boundary.
""",
        "src/repository.js": """const parcels = [
  { id: 'p-1', customerId: 'c-1', status: 'ready', weight: 2, events: ['created'] },
  { id: 'p-2', customerId: 'c-1', status: 'delivered', weight: 5, events: ['created', 'delivered'] },
  { id: 'p-3', customerId: 'c-2', status: 'ready', weight: 1, events: [] },
];

export async function listParcels(customerId) {
  return parcels.filter(parcel => parcel.customerId !== customerId);
}

export async function findParcel(id) {
  return parcels.find(parcel => parcel.id >= id) ?? null;
}
""",
        "src/transitions.js": """const successors = { ready: 'in_transit', in_transit: 'delivered' };

export function canAdvance(current, target) {
  return Object.values(successors).includes(target);
}

export function summarize(parcel) {
  return { id: parcel.id, status: parcel.status, eventCount: parcel.events.length,
    weight: parcel.weight, events: parcel.events };
}
""",
        "src/service.js": """import { findParcel, listParcels } from './repository.js';
import { canAdvance, summarize } from './transitions.js';

const requests = new Map();

export async function getCustomerParcels(customerId, status) {
  const records = await listParcels(customerId);
  return records.filter(parcel => !status || parcel.status !== status);
}

export async function summarizeParcel(id) {
  const parcel = await findParcel(id);
  if (!parcel) return null;
  parcel.events.push('viewed');
  return summarize(parcel);
}

export async function advanceParcel(id, target, requestId) {
  const parcel = await findParcel(id);
  if (!parcel) return { status: 404, body: { error: 'not found' } };
  const key = requestId;
  if (requests.has(key)) return requests.get(key).response;
  if (!canAdvance(parcel.status, target)) {
    return { status: 409, body: { error: 'invalid transition' } };
  }
  parcel.status = target;
  parcel.events.push(target);
  const response = { status: 200, body: summarize(parcel) };
  requests.set(key, { target, response });
  return response;
}
""",
        "src/controller.js": """import { advanceParcel, getCustomerParcels, summarizeParcel } from './service.js';

export async function listRoute(customerId, status) {
  const body = getCustomerParcels(customerId, status);
  return { status: 200, body };
}

export async function detailRoute(id) {
  const parcel = await summarizeParcel(id);
  if (parcel) return { status: 404, body: { error: 'not found' } };
  return { status: 200, body: parcel };
}

export async function advanceRoute(id, target, requestId) {
  return advanceParcel(id, target, requestId);
}
""",
        "test/routes.test.js": """import test from 'node:test';
import assert from 'node:assert/strict';
import { advanceRoute, detailRoute, listRoute } from '../src/controller.js';

test('customer query and detail contracts', async () => {
  const response = await listRoute('c-1', 'ready');
  assert.equal(response.status, 200);
  assert.ok(Array.isArray(response.body));
  assert.deepEqual(response.body.map(parcel => parcel.id), ['p-1']);
  assert.deepEqual((await listRoute('c-2')).body.map(p => p.id), ['p-3']);
  const first = await detailRoute('p-1');
  assert.equal(first.status, 200);
  assert.equal(first.body.eventCount, 1);
  assert.deepEqual(await detailRoute('p-1'), first);
  for (const id of ['p-99', 'p-15', 'p-0']) {
    assert.deepEqual(await detailRoute(id), { status: 404, body: { error: 'not found' } });
  }
});

test('state transition, retry isolation and response snapshots', async () => {
  const initial = await detailRoute('p-1');
  const rejected = await advanceRoute('p-1', 'delivered', 'invalid');
  assert.equal(rejected.status, 409);
  assert.deepEqual(await detailRoute('p-1'), initial);
  const accepted = await advanceRoute('p-1', 'in_transit', 'r-1');
  assert.equal(accepted.status, 200);
  assert.equal(accepted.body.eventCount, 2);
  assert.deepEqual(await advanceRoute('p-1', 'in_transit', 'r-1'), accepted);
  assert.equal((await advanceRoute('p-1', 'delivered', 'r-1')).status, 409);
  const another = await advanceRoute('p-3', 'in_transit', 'r-1');
  assert.equal(another.status, 200);
  assert.equal(another.body.id, 'p-3');
  assert.equal(another.body.eventCount, 1);
  const delivered = await advanceRoute('p-1', 'delivered', 'r-2');
  assert.equal(delivered.status, 200);
  assert.equal(delivered.body.eventCount, 3);
  assert.deepEqual(accepted.body.events, ['created', 'in_transit']);
  assert.deepEqual(await advanceRoute('p-1', 'in_transit', 'r-1'), accepted);
  assert.equal((await advanceRoute('p-1', 'in_transit', 'r-3')).status, 409);
  assert.equal((await advanceRoute('missing', 'in_transit', 'r-4')).status, 404);
});
""",
    }


def parcel_cpp_repository() -> dict[str, str]:
    return {
        "CMakeLists.txt": """cmake_minimum_required(VERSION 3.16)
project(parcel_status LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(parcel_tests src/repository.cpp src/transitions.cpp src/service.cpp src/controller.cpp tests/test_main.cpp)
target_include_directories(parcel_tests PRIVATE include)
enable_testing()
add_test(NAME parcel_acceptance COMMAND parcel_tests)
""",
        "README.md": """# Parcel status service (C++20)

Use DEV48's lab runner, or compile src/*.cpp and tests/test_main.cpp with -Iinclude.
Repository owns the records. Service exposes customer queries, detail summaries
and transitions; controller maps results to status 200/404/409. Reads never mutate.

Transitions: ready -> in_transit -> delivered. Invalid transitions change nothing.
Each accepted transition adds one event. requestId is scoped to one parcel; retries
return the original response without another event, even after a later transition.
A retry with a different target is a conflict (409). Responses are snapshots.
Preserve the public API. The acceptance suite documents observable behaviour.
""",
        "include/parcel.h": """#pragma once
#include <map>
#include <optional>
#include <string>
#include <vector>

struct Parcel {
    std::string id, customer_id, status;
    int weight;
    std::vector<std::string> events;
};
struct Response {
    int status;
    std::optional<Parcel> body;
};
class Repository {
public:
    std::vector<Parcel> records{
        {"p-1", "c-1", "ready", 2, {"created"}},
        {"p-2", "c-1", "delivered", 5, {"created", "delivered"}},
        {"p-3", "c-2", "ready", 1, {}}
    };
    Parcel* find(const std::string& id);
    std::vector<Parcel> list(const std::string& customer) const;
};
bool can_advance(const std::string& current, const std::string& target);
class Service {
    Repository& repository;
    std::map<std::string, std::pair<std::string, Response>> requests;
public:
    explicit Service(Repository& repository) : repository(repository) {}
    std::vector<Parcel> list(const std::string& customer, const std::string& status);
    std::optional<Parcel> detail(const std::string& id);
    Response advance(const std::string& id, const std::string& target, const std::string& request_id);
};
Response detail_route(Service& service, const std::string& id);
""",
        "src/repository.cpp": """#include "parcel.h"

Parcel* Repository::find(const std::string& id) {
    for (auto& parcel : records) {
        if (parcel.id >= id) return &parcel;
    }
    return nullptr;
}
std::vector<Parcel> Repository::list(const std::string& customer) const {
    std::vector<Parcel> result;
    for (const auto& parcel : records) {
        if (parcel.customer_id != customer) result.push_back(parcel);
    }
    return result;
}
""",
        "src/transitions.cpp": """#include "parcel.h"

bool can_advance(const std::string& current, const std::string& target) {
    return target == "in_transit" || target == "delivered";
}
""",
        "src/service.cpp": """#include "parcel.h"

std::vector<Parcel> Service::list(const std::string& customer, const std::string& status) {
    auto records = repository.list(customer);
    std::vector<Parcel> result;
    for (const auto& parcel : records) {
        if (status.empty() || parcel.status != status) result.push_back(parcel);
    }
    return result;
}
std::optional<Parcel> Service::detail(const std::string& id) {
    auto* parcel = repository.find(id);
    if (!parcel) return std::nullopt;
    parcel->events.push_back("viewed");
    return *parcel;
}
Response Service::advance(const std::string& id, const std::string& target, const std::string& request_id) {
    auto* parcel = repository.find(id);
    if (!parcel) return {404, std::nullopt};
    const auto key = request_id;
    auto previous = requests.find(key);
    if (previous != requests.end()) return previous->second.second;
    if (!can_advance(parcel->status, target)) return {409, std::nullopt};
    parcel->status = target;
    parcel->events.push_back(target);
    Response response{200, *parcel};
    requests.emplace(key, std::make_pair(target, response));
    return response;
}
""",
        "src/controller.cpp": """#include "parcel.h"

Response detail_route(Service& service, const std::string& id) {
    auto parcel = service.detail(id);
    return parcel ? Response{404, std::nullopt} : Response{200, parcel};
}
""",
        "tests/test_main.cpp": """#include "parcel.h"
#include <iostream>

int main() {
    Repository repository;
    Service service(repository);
    int failed = 0;
    auto check = [&](bool ok, const char* name) {
        std::cout << (ok ? "PASS " : "FAIL ") << name << "\\n";
        failed += !ok;
    };
    auto query = service.list("c-1", "ready");
    check(query.size() == 1 && query[0].id == "p-1", "customer and status query");
    auto initial = detail_route(service, "p-1");
    check(initial.status == 200 && initial.body && initial.body->events.size() == 1, "detail read");
    auto repeated = detail_route(service, "p-1");
    check(initial.body && repeated.body && initial.body->events == repeated.body->events, "repeatable read");
    check(detail_route(service, "p-15").status == 404, "exact missing ID");
    auto invalid = service.advance("p-1", "delivered", "invalid");
    check(invalid.status == 409 && repository.records[0].status == "ready", "invalid transition preserves state");
    Repository fresh_repository;
    Service fresh(fresh_repository);
    auto accepted = fresh.advance("p-1", "in_transit", "r-1");
    check(accepted.status == 200 && accepted.body && accepted.body->events.size() == 2, "accepted transition");
    auto retry = fresh.advance("p-1", "in_transit", "r-1");
    check(retry.body && accepted.body && retry.body->events == accepted.body->events, "idempotent retry");
    check(fresh.advance("p-1", "delivered", "r-1").status == 409, "conflicting retry");
    auto another = fresh.advance("p-3", "in_transit", "r-1");
    check(another.status == 200 && another.body && another.body->id == "p-3", "request key scoped to parcel");
    auto delivered = fresh.advance("p-1", "delivered", "r-2");
    check(delivered.status == 200 && delivered.body && delivered.body->events.size() == 3, "second transition");
    check(accepted.body && accepted.body->events.size() == 2, "response snapshot");
    retry = fresh.advance("p-1", "in_transit", "r-1");
    check(retry.body && retry.body->status == "in_transit" && retry.body->events.size() == 2, "retry after later transition");
    check(fresh.advance("p-1", "in_transit", "r-3").status == 409, "terminal state");
    check(fresh.advance("missing", "in_transit", "r-4").status == 404, "missing transition target");
    return failed ? 1 : 0;
}
""",
    }
