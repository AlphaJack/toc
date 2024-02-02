// ┌───────────────────────────────────────────────────────────────┐
// │ Contents of carbon_complex.carbon                             │
// ├───────────────────────────────────────────────────────────────┘
// │
// ├──┐Nested 1
// │  └──┐Nested 2
// │     └──┐Nested 3
// │        ├── Nested 4
// │        ├──┐Nested 4
// │        │  ├──┐Nested 5
// │        │  │  ├── Nested 6
// │        │  │  └── Nested 6
// │        │  └──┐Nested 5
// │        │     └── Nested 6
// │        ├── Nested 4
// │        └── Nested 4
// │
// └───────────────────────────────────────────────────────────────

// ################################################################ Nested 1

package ExplorerTest api;

fn Main() -> i32 {
  var s: auto = "Hello world!";
  Print(s);
  return 0;
}

// ################################ Nested 2

// ################ Nested 3

// ######## Nested 4

// ######## Nested 4

// #### Nested 5

// ## Nested 6
// ## Nested 6

// #### Nested 5

// ## Nested 6

// ######## Nested 4

// ######## Nested 4
