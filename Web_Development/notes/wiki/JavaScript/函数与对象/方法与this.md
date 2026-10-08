---
tags: [WD, 对象, 方法, this, 箭头函数]
domain: [Web 应用开发, JavaScript 函数与对象]
course: COMP3421
lecture: L06
---

# 方法与 this · Methods and `this`

> **一句话**：`this` 指的是**这次调用发生在哪个对象上** —— 不是定义的地方，是**点号左边那个东西**；箭头函数**不创建自己的 `this`**，所以写对象方法必须用 `function` 而不是箭头函数。

课件原文见 [Lecture_06_JS.pptx](<../../../raw/Lecture_06_JS.pptx>)。本篇覆盖 §6 Objects 的 Object Methods and `this` 一页：方法是什么、`this` 归谁、以及箭头函数为什么不能拿来写方法。

## 一、方法就是存在属性上的函数

课件的定义很朴素：*A method is a **function in a property** — what is stored there is a function definition.*

```js
const person = {
  firstName: "John",
  lastName: "Doe",
  fullName: function () {
    return this.firstName + " " + this.lastName;
  }
};
```

`fullName` 这个属性存的是一个函数。**和普通函数没有任何语法差别** —— 它只是恰好被放在对象里，于是我们管它叫方法。

## 二、`this` 是调用所在的那个对象

课件的定义：***`this` is the owner — inside the method, `this` is the object the call was made on.***

```js
person.fullName();   // "John Doe"
```

调用是 `person.fullName()`，**点号左边是 `person`**，所以方法体里的 `this` 就是 `person`。
于是 `this.firstName` 读出 `"John"`，`this.lastName` 读出 `"Doe"`，拼成 `"John Doe"`。

> [!important] 关键一句：**是调用决定的，不是定义决定的**
> `this` 在函数**被调用**的那一刻才确定下来，取决于你是**从谁身上**调它的。
> 同一个函数，从 `person` 上调，`this` 就是 `person`；从 `teacher` 上调，`this` 就是 `teacher`。
>
> 这也是"方法"和"一个恰好存在属性上的普通函数"在**运行结果**上的唯一差别 ——
> 是这次调用给了它 `this`。

## 三、必须用点号调

课件特意写了一条：***Call it with the dot — `person.fullName()` — **the call is what fixes `this`**.***

点号不是"语法上更漂亮"，它是**把 `this` 钉住**的那一步。写成下面这样，方法会跑，但 `this` 就不是 `person` 了：

```js
const f = person.fullName;
f();               // ✗ this 丢了 —— f 是个独立的函数，不再"属于" person
person.fullName(); // ✅ this === person
```

拆开看就是"**谁提供这次调用**"这个问题。把方法从对象上摘下来单独存，调用时就没人提供主人了。

## 四、箭头函数不绑定 `this`

课件加的限定句：***Arrow functions do not bind `this` — they take it from the surrounding code, so **use the function form for a method**.** 箭头函数**不绑定 `this`**，它从周围的代码继承 `this`。所以**方法要用 `function` 写法**。

```js
const bad = {
  firstName: "John",
  lastName: "Doe",
  fullName: () => {
    return this.firstName + " " + this.lastName;   // ✗
  }
};
bad.fullName();   // 拿不到 firstName
```

箭头函数里写 `this`，拿到的是**它被写下的那个位置的外层 `this`**，而不是 `bad`。

| | `function` 写法 | 箭头函数写法 |
|---|---|---|
| 方法里的 `this` | 调用所在的对象 | 写它的地方的外层 `this` |
| 适合写方法吗 | ✅ | ✗ |

判断办法很简单：**这个函数需不需要知道自己被谁调用？** 需要就用 `function`。

> [!warning] 本讲的 `this` 只讲到这一层
> 课件在这一页讲的是"`this` 是调用所在的那个对象"，然后就在结尾把后续内容交给了
> **Week 7 — JavaScript II: `this`, prototypes, classes and closures**。
>
> 那份课件**还不在 `notes/raw/` 里**，所以本库**不补写**以下内容：
> `this` 在函数被单独调用时（不带点号）指向哪里、`this` 在普通函数里指向 `window`、
> `bind` / `call` / `apply`、箭头函数里 `this` 为什么取外层、**原型链**与 `class`、
> 以及**闭包**。这些属于 Week 7，等课件补进来之后再写。
>
> 同一处留白见 [[作用域与严格模式]]（严格模式对 `this` 的影响）和
> [[函数即值]]（箭头函数不创建自己的 `this`）。

## 五、`this` 和箭头函数在别处的用处

虽然**方法里**不能用箭头函数，但箭头函数在别处很方便 —— 只要它**不需要 `this`**：

```js
btn.addEventListener("click", () => {
  console.log("我不需要知道是谁点的");
});
```

如果确实需要触发事件的元素，那用的是**事件对象的 `target`**，不是 `this` —— 详见 [[事件监听器]]。

## 关联

- 属性容器 → [[对象与属性]]（方法就是存在属性上的函数，容器本身在那篇）
- 箭头函数 → [[函数即值]]（箭头函数是函数表达式的一种，它的不绑定 `this` 在那里也提了一句）
- 调用与 `this` → [[定义与调用]]（`()` 才是调用，点号把 `this` 钉住）
- 失去主人 → [[作用域与严格模式]]（函数被摘出来单独调用，与"漏写声明造全局"是同一类问题）
- Week 7 留白 → [[课程场景与阅读约定]]（原型、`class`、闭包为什么本库不写）
- 事件里的"谁触发的" → [[事件监听器]]（用 `event.target` 而不是 `this`）
