---
source: "https://usefulcheatsheets.com/technology/typescript/typescript-advanced-types"
title: "TypeScript Advanced Types | Useful Cheatsheets"
fetched_at: "2026-10-06 12:32"
---

[Build](/build) / [Code](/build/code) / [TypeScript](/build/code/typescript)

# TypeScript Advanced Types

A comprehensive guide to conditional types, mapped types, template literals, and type inference with infer.

## TL;DR

  1. 1Build type-level ternary conditions using the `extends ? :` syntax.
  2. 2Extract nested types automatically with the conditional `infer` keyword.
  3. 3Transform object keys dynamically using mapped type `as` remapping clauses.



Jump to section

  * #Conditional Types
  * #Type Inference with Infer
  * #Mapped Types
  * #Key Remapping with As
  * #Template Literal Types
  * #Tips
  * #Warnings
  * #In Practice
  * #FAQ



## Conditional Types

`ternary syntax`

Evaluates type-level branching based on contract assignability.
    
    type IsString<T> = T extends string ? true : false;
    type A = IsString<'hello'>; 
    type B = IsString<number>;  

`distributive conditional`

Applies conditional logic across each member of a union.
    
    type Box<T> = T extends any ? { val: T } : never;
    type Boxed = Box<string | number>;
    

`preventing distribution`

Wraps type in a tuple to evaluate unions as a single entity.
    
    type NonDistributive<T> = [T] extends [string]
      ? true
      : false;
    type Check = NonDistributive<string | number>; 




## Type Inference with Infer

`infer return type`

Extracts the return type of an arbitrary function signature.
    
    type GetReturn<T> = T extends (
      ...args: any[]
    ) => infer R ? R : never;
    type Num = GetReturn<() => number>; 

`unwrap Promise`

Extracts the resolved payload type from Promise instances.
    
    type Unwrap<T> = T extends Promise<infer U> ? U : T;
    type Resolved = Unwrap<Promise<string>>; 

`tuple element extraction`

Pulls out the first element type from fixed tuple arrays.
    
    type Head<T> = T extends [infer First, ...any[]]
      ? First
      : never;
    type First = Head<[string, number]>; 




## Mapped Types

`mapped key iteration`

Iterates over property keys of an object to transform types.
    
    type Stringify<T> = {
      [K in keyof T]: string;
    };
    type Base = { age: number; active: boolean };
    type Form = Stringify<Base>;

`modifier subtraction`

Removes readonly and optional flags with minus prefixes.
    
    type Concrete<T> = {
      -readonly [K in keyof T]-?: T[K];
    };

`filtering with never`

Excludes properties whose keys map to the never type.
    
    type OnlyStrings<T> = {
      [K in keyof T as
        T[K] extends string ? K : never]: T[K];
    };




## Key Remapping with As

`getter remapping`

Generates getter function signatures with capitalized keys.
    
    type Getters<T> = {
      [K in keyof T as `get${Capitalize<string & K>}`]:
        () => T[K];
    };
    type PersonGetters = Getters<{ name: string }>;

`prefixing keys`

Prepends a common namespace prefix to all property keys.
    
    type Prefixed<T, P extends string> = {
      [K in keyof T as `${P}_${string & K}`]: T[K];
    };

`filter by value type`

Keeps only properties whose values match a given constraint.
    
    type MethodsOnly<T> = {
      [K in keyof T as T[K] extends Function ? K : never]:
        T[K];
    };




## Template Literal Types

`string union cross-product`

Combines string unions into combinatorial variations.
    
    type Event = 'click' | 'focus';
    type State = 'active' | 'idle';
    type EventState = `${Event}_${State}`;
    

`intrinsic string helpers`

Transforms casing with Uppercase and Capitalize helpers.
    
    type Shout = Uppercase<'hello'>; 
    type Cap = Capitalize<'name'>;    

`pattern matching strings`

Extracts substrings dynamically using infer inside literals.
    
    type TrimPrefix<T> = T extends `prefix_${infer Rest}`
      ? Rest
      : T;
    type Clean = TrimPrefix<'prefix_item'>; 




## Tips

  1. 1Wrap naked type parameters in single-element tuples like `[T]` to prevent distributive behavior across union types.
  2. 2Combine template literal types with `Capitalize` to auto-generate type-safe getter and setter signatures from existing property names.



## Warnings

  1. 1Avoid unbounded recursive conditional types using `infer` because exceeding the compiler recursion limit causes fatal stack overflow errors.
  2. 2Remember that mapped types filtering keys with `never` only remove keys when using the `as` key remapping clause.



## In Practice

Combines template literal types, mapped key remapping, and conditional inference to generate event handler interfaces.

  1. 1Define an object mapping event names to their payload structures.
  2. 2Use mapped key remapping with Capitalize to construct 'on' listener names.
  3. 3Derive handler callback parameters from original event payload shapes.
  4. 4Implement a typed emitter guaranteeing compile-time event verification.


    
    
    interface Events {
      login: { user: string };
      logout: { user: string };
    }
    
    type Listeners<T> = {
      [K in keyof T as `on${Capitalize<string & K>}`]: (
        payload: T[K]
      ) => void;
    };
    
    type AppListeners = Listeners<Events>;
    
    const emitter: AppListeners = {
      onLogin: (e) => console.log(`In: ${e.user}`),
      onLogout: (e) => console.log(`Out: ${e.user}`)
    };
    
    emitter.onLogin({ user: 'ada' });

## FAQ

The `infer` keyword introduces a variable inside the true branch of a conditional type that captures an unknown inner type. When TypeScript matches the pattern, it binds that extracted type variable, enabling operations like unwrapping Promise resolutions or function returns.

When a generic type parameter `T` is checked directly as `T extends U ? X : Y` and a union like `string | number` is passed, TypeScript distributes the conditional over each union member individually (`(string extends U ? ...) | (number extends U ? ...)`).
    
    
    type ToArray<T> = T extends any ? T[] : never;
    type Res = ToArray<string | number>; 

Add `as` after the mapped key iteration, such as `[K in keyof T as NewKey]: T[K]`. You can use template literals to prefix key names or conditional types returning `never` to filter unwanted properties out of the resulting type entirely.

By interpolating unions or primitives into backticks, e.g. `type Route = `/${string}``. The compiler enforces that any assigned string conforms to the specified pattern, rejecting invalid paths and preventing malformed string identifiers at compile time.
