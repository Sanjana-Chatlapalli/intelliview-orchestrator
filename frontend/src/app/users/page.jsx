"use client";

import { useMemo, useState } from "react";
import { Search, Plus, Pencil, Trash2, User } from "lucide-react";

const initialUsers = [
  {
    id: 1,
    name: "Aswini",
    email: "aswini@example.com",
    role: "Admin",
    status: "Active",
  },
  {
    id: 2,
    name: "Rahul",
    email: "rahul@example.com",
    role: "User",
    status: "Active",
  },
];

export default function UsersPage() {
  const [users, setUsers] = useState(initialUsers);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    role: "User",
  });

  const filteredUsers = useMemo(() => {
    const value = search.toLowerCase();

    return users.filter(
      (user) =>
        user.name.toLowerCase().includes(value) ||
        user.email.toLowerCase().includes(value) ||
        user.role.toLowerCase().includes(value)
    );
  }, [users, search]);

  function handleSubmit(e) {
    e.preventDefault();

    if (!form.name.trim() || !form.email.trim()) {
      return;
    }

    const newUser = {
      id: users.length + 1,
      name: form.name,
      email: form.email,
      role: form.role,
      status: "Active",
    };

    setUsers((current) => [...current, newUser]);

    setForm({
      name: "",
      email: "",
      role: "User",
    });

    setShowForm(false);
  }

  function deleteUser(id) {
    setUsers((current) => current.filter((user) => user.id !== id));
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-zinc-50">
            User Management
          </h1>

          <p className="mt-1 text-sm text-muted">
            Manage users and their access roles.
          </p>
        </div>

        <button
          onClick={() => setShowForm(true)}
          className="inline-flex items-center justify-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition hover:opacity-90"
        >
          <Plus size={16} />
          Add User
        </button>
      </div>

      {/* Search */}
      <div className="glass-card p-4">
        <div className="relative max-w-md">
          <Search
            size={17}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-muted"
          />

          <input
            type="text"
            placeholder="Search users..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-md border border-border bg-bg-card py-2 pl-10 pr-3 text-sm text-zinc-100 outline-none placeholder:text-muted focus:border-accent"
          />
        </div>
      </div>

      {/* Add User Form */}
      {showForm && (
        <div className="glass-card p-5">
          <div className="mb-4 flex items-center gap-2">
            <User size={18} />
            <h2 className="text-lg font-medium text-zinc-50">
              Add New User
            </h2>
          </div>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-4 md:grid-cols-3"
          >
            <input
              type="text"
              placeholder="Full name"
              value={form.name}
              onChange={(e) =>
                setForm({ ...form, name: e.target.value })
              }
              className="rounded-md border border-border bg-bg-card px-3 py-2 text-sm text-zinc-100 outline-none placeholder:text-muted focus:border-accent"
            />

            <input
              type="email"
              placeholder="Email address"
              value={form.email}
              onChange={(e) =>
                setForm({ ...form, email: e.target.value })
              }
              className="rounded-md border border-border bg-bg-card px-3 py-2 text-sm text-zinc-100 outline-none placeholder:text-muted focus:border-accent"
            />

            <select
              value={form.role}
              onChange={(e) =>
                setForm({ ...form, role: e.target.value })
              }
              className="rounded-md border border-border bg-bg-card px-3 py-2 text-sm text-zinc-100 outline-none focus:border-accent"
            >
              <option value="User">User</option>
              <option value="Admin">Admin</option>
              <option value="HR">HR</option>
            </select>

            <div className="flex gap-2 md:col-span-3">
              <button
                type="submit"
                className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white hover:opacity-90"
              >
                Create User
              </button>

              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="rounded-md border border-border px-4 py-2 text-sm text-zinc-300 hover:bg-bg-card"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Users Table */}
      <div className="glass-card overflow-hidden">
        <div className="border-b border-border px-5 py-4">
          <h2 className="font-medium text-zinc-50">Users</h2>
          <p className="text-xs text-muted">
            {filteredUsers.length} user
            {filteredUsers.length !== 1 ? "s" : ""} found
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-border text-xs uppercase text-muted">
                <th className="px-5 py-3">ID</th>
                <th className="px-5 py-3">Name</th>
                <th className="px-5 py-3">Email</th>
                <th className="px-5 py-3">Role</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>

            <tbody>
              {filteredUsers.length === 0 ? (
                <tr>
                  <td
                    colSpan="6"
                    className="px-5 py-10 text-center text-muted"
                  >
                    No users found.
                  </td>
                </tr>
              ) : (
                filteredUsers.map((user) => (
                  <tr
                    key={user.id}
                    className="border-b border-border last:border-0 hover:bg-bg-card/60"
                  >
                    <td className="px-5 py-4 font-mono text-xs text-zinc-400">
                      {user.id}
                    </td>

                    <td className="px-5 py-4 font-medium text-zinc-100">
                      {user.name}
                    </td>

                    <td className="px-5 py-4 text-zinc-400">
                      {user.email}
                    </td>

                    <td className="px-5 py-4">
                      <span className="rounded-full border border-border px-2.5 py-1 text-xs text-zinc-300">
                        {user.role}
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <span className="rounded-full bg-emerald-500/10 px-2.5 py-1 text-xs text-emerald-400">
                        {user.status}
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <div className="flex justify-end gap-2">
                        <button
                          className="rounded-md border border-border p-2 text-zinc-400 hover:text-white"
                          title="Edit user"
                        >
                          <Pencil size={15} />
                        </button>

                        <button
                          onClick={() => deleteUser(user.id)}
                          className="rounded-md border border-border p-2 text-zinc-400 hover:text-red-400"
                          title="Delete user"
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}