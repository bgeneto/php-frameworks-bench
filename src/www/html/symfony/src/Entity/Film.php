<?php

namespace App\Entity;

use App\Repository\FilmRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: FilmRepository::class)]
class Film
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255)]
    private ?string $title = null;

    #[ORM\Column(type: Types::TEXT, nullable: true)]
    private ?string $description = null;

    #[ORM\Column(nullable: true)]
    private ?int $release_year = null;

    #[ORM\Column(nullable: true)]
    private ?int $rental_duration = null;

    #[ORM\Column(type: Types::DECIMAL, precision: 5, scale: 2, nullable: true)]
    private ?string $rental_rate = null;

    #[ORM\Column(nullable: true)]
    private ?int $length = null;

    #[ORM\Column(type: Types::DECIMAL, precision: 5, scale: 2, nullable: true)]
    private ?string $replacement_cost = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $rating = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $special_features = null;

    #[ORM\Column(type: Types::DATETIME_MUTABLE, nullable: true)]
    private ?\DateTimeInterface $last_update = null;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getTitle(): ?string
    {
        return $this->title;
    }

    public function setTitle(string $title): static
    {
        $this->title = $title;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): static
    {
        $this->description = $description;

        return $this;
    }

    public function getReleaseYear(): ?int
    {
        return $this->release_year;
    }

    public function setReleaseYear(?int $release_year): static
    {
        $this->release_year = $release_year;

        return $this;
    }

    public function getRentalDuration(): ?int
    {
        return $this->rental_duration;
    }

    public function setRentalDuration(?int $rental_duration): static
    {
        $this->rental_duration = $rental_duration;

        return $this;
    }

    public function getRentalRate(): ?string
    {
        return $this->rental_rate;
    }

    public function setRentalRate(?string $rental_rate): static
    {
        $this->rental_rate = $rental_rate;

        return $this;
    }

    public function getLength(): ?int
    {
        return $this->length;
    }

    public function setLength(?int $length): static
    {
        $this->length = $length;

        return $this;
    }

    public function getReplacementCost(): ?string
    {
        return $this->replacement_cost;
    }

    public function setReplacementCost(?string $replacement_cost): static
    {
        $this->replacement_cost = $replacement_cost;

        return $this;
    }

    public function getRating(): ?string
    {
        return $this->rating;
    }

    public function setRating(?string $rating): static
    {
        $this->rating = $rating;

        return $this;
    }

    public function getSpecialFeatures(): ?string
    {
        return $this->special_features;
    }

    public function setSpecialFeatures(?string $special_features): static
    {
        $this->special_features = $special_features;

        return $this;
    }

    public function getLastUpdate(): ?\DateTimeInterface
    {
        return $this->last_update;
    }

    public function setLastUpdate(?\DateTimeInterface $last_update): static
    {
        $this->last_update = $last_update;

        return $this;
    }
}
