package com.example.producergui.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Product
{
    private Integer id;
    private String name;
    private String description;
    private Double price;

    public Product(int id, String name, String description)
    {
        this.id = id;
        this.name = name;
        this.description = description;
    }

    public Product(int id, String name, String description, double price)
    {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
    }
}
